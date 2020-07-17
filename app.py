from config import StEdwardsConfig
from utils import db
from bootstrap.db import bootstrap
from bootstrap.jinja import prep_jinja

from models.assignment import Assignment
from models.course import Course
from models.instructor import Instructor
from models.student import Student
from models.enrollment import Enrollment
from models.grade import Grade
from lms.lms import Canvas as LmsClass

from collections import defaultdict
import datetime
from logzero import logger


if __name__ == '__main__':
    logger.info('Starting...')
    config = StEdwardsConfig

    # Bootstrap if needed and get the connection and a cursor
    conn, cursor = bootstrap(config, db)
    SCHOOL_QUERY = '''SELECT api_url FROM schools WHERE id = %s'''
    params = (config.SCHOOL_ID,)
    school = db.run_query(SCHOOL_QUERY, cursor, params)[0]
    api_url = school['api_url']
    logger.info('School api url retrieved')

    # Used for testing, delete later
    ref_date = config.REF_DATE
    logger.info(f'Using ref_date {ref_date}')

    # Get the instructors who have active course instances
    INSTRUCTORS_QUERY = '''SELECT i.* 
                            FROM instructors i JOIN schools s on i.school_id = s.id
                            WHERE s.id = %s;'''
    params = (config.SCHOOL_ID,)
    instructors = db.run_query(INSTRUCTORS_QUERY, cursor, params)
    logger.info(f'{len(instructors)} instructors found in db with active course instance')
    for i in instructors:
        # Connect to the instructors Canvas account
        lms_token = i['lms_token']
        lms_obj = LmsClass(config.LMS_URL, lms_token, api_url)

        # Create the instructor object from db info and grab all their courses from db
        instructor = Instructor(first_name=i['first_name'],
                                last_name=i['last_name'],
                                email=i['email'],
                                lms_id=i['lms_id'])
        INSTRUCTOR_COURSES = f'''SELECT DISTINCT lms_id, name 
                                FROM courses
                                WHERE instructor_id = %s'''
        params = (i['id'],)
        instructor_courses_dict = db.run_query(INSTRUCTOR_COURSES, cursor, params)
        instructor.add_courses([Course(lms_id=c['canvas_id'], name=c['name']) for c in instructor_courses_dict])

        for course in instructor.courses:
            # Get the students, enrollments, assigments, and grades for this course
            students_dict = lms_obj.get_students_in_course(course.lms_id)
            students = [Student(student['name'], student['lms_id']) for student in students_dict]
            course.add_students(students)

            assignments_dict = lms_obj.get_course_assignments(course.lms_id)
            # Check to make sure the course actually has assignments (for example, MATH 4157 does not),
            # then add them to the course object
            if not assignments_dict:
                assignments = []
            else:
                assignments = [Assignment(assignment['lms_id'],
                                          assignment['name'],
                                          assignment['due_date'],
                                          course) for assignment in assignments_dict]
            course.add_assignments(assignments)

            # Get grades for all assignments
            grades_dict = lms_obj.get_course_grades(course.lms_id, students, assignments)
            # Get overall grades for all students (cumulative grade)
            current_scores_dict = lms_obj.get_current_scores(course.lms_id)
            # Create an Enrollment object for each student with all of their assignments, along with their current grade
            for student in students:
                enrollment = Enrollment(student, course, current_score=current_scores_dict.get(student.lms_id))
                student_grades = []
                for assignment in assignments:
                    # Find the entry in grades_dict corresponding to this assignment
                    assignment_score = [a for a in grades_dict.get(student) if a['lms_id'] == assignment.lms_id]
                    if assignment_score:
                        student_grades.append(Grade(student, course, assignment, assignment_score[0].get('score')))
                enrollment.add_grades(student_grades)
                student.add_enrollments(enrollment)

        # Context dictionaries are used by Jinja to create the emails
        course_context_dicts = []
        # Used for testing since there are no current assignments
        for course in instructor.courses:
            course_outliers = defaultdict(list)
            for student in course.students:
                # Create CI's for each student -> floats
                enrollment = student.get_enrollment_by_course(course)
                enrollment.form_ci(distribution=config.DISTRIBUTION)

                # Look for new good/bad results -> Assignments
                outlier_assignments = enrollment.get_outliers(ref_date=ref_date)

                # Create student summary -> list of Assignments
                if outlier_assignments:
                    course_outliers[enrollment] = outlier_assignments
                    if config.COMMIT_OUTLIERS_TO_DB:
                        enrollment.commit_outliers_to_db(outlier_assignments, cursor, conn)

            # Create class summary (mean/median class grade)
            summary_stat = config.COURSE_SUMMARY_STAT
            summary_stat_value = lms_obj.get_course_grade_summary(course.lms_id, summary_stat)
            course_summary = {'summary_stat': summary_stat, 'summary_stat_value': summary_stat_value}

            # Craft (email) card for this course
            env = prep_jinja()
            course_card = course.context_dict(course_outliers, course_summary)
            course_context_dicts.append(course_card)

        # Send email
        context_dict = {'context_dicts': course_context_dicts,
                        'instructor': instructor,
                        'current_date': datetime.datetime.now(),
                        'week_start': datetime.datetime.now() - datetime.timedelta(days=6)
                        }
        email = instructor.render_email(context_dict, env)
        instructor.send_email(email)
        logger.info(f'{len(instructor.courses)} courses processed for instructor {instructor.email}')
