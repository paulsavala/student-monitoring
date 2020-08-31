from utils import db
from bootstrap.db import bootstrap
from bootstrap.jinja import prep_jinja

from models.assignment import Assignment
from models.course import Course
from models.instructor import Instructor
from models.student import Student
from models.enrollment import Enrollment
from models.grade import Grade
import config

from collections import defaultdict
import datetime
from logzero import logger
import os


if __name__ == '__main__':
    logger.info('Starting...')

    # Bootstrap if needed and get the connection and a cursor
    conn, cursor = bootstrap(config.GenericConfig.DB_ENDPOINT, db)
    logger.info('Connected to database')
    # Get all schools
    SCHOOL_QUERY = 'SELECT DISTINCT id FROM schools;'
    schools = db.run_query(SCHOOL_QUERY, cursor)
    logger.info(f'{len(schools)} schools retrieved')
    for school_id in schools:
        logger.info(f'Processing school {school_id}')
        if os.environ.get('TESTING'):
            logger.info('====== TESTING MODE ========')
            SCHOOL_API_QUERY = '''SELECT DISTINCT config_test_class_name AS "config_class" FROM schools WHERE id = %s;'''
        else:
            SCHOOL_API_QUERY = '''SELECT DISTINCT config_class_name AS "config_class" FROM schools WHERE id = %s;'''
        params = (school_id['id'],)
        school_info = db.run_query(SCHOOL_API_QUERY, cursor, params)
        if len(school_info) > 1:
            logger.error(f'Multiple entries found for school with id {school_id["id"]}, using first')
        school_info = school_info[0]
        school_config = getattr(config, school_info['config_class'])
        logger.info('School config class retrieved')

        # Get the school LMS
        LmsClass = school_config.LMS

        # Used for testing
        ref_date = os.environ.get('REF_DATE')
        if ref_date is not None:
            logger.info(f'Using ref_date {ref_date}')
            try:
                ref_date = datetime.datetime.strptime(ref_date, '%Y-%m-%d')
            except ValueError as e:
                logger.error(f'Invalid ref_date. Must be in the form %Y-%m-%d, ignoring')
                ref_date = None

        # Get the instructors who have active course instances
        # If in testing mode, only grab admins
        if school_config.TESTING:
            logger.info('Testing mode, only sending emails to admins')
            INSTRUCTORS_QUERY = '''SELECT DISTINCT i.* 
                                    FROM instructors i JOIN schools s on i.school_id=s.id
                                    JOIN courses c on c.instructor_id=i.id
                                    WHERE s.id=%s AND c.is_monitored=TRUE AND i.is_admin=TRUE;'''
        else:
            INSTRUCTORS_QUERY = '''SELECT DISTINCT i.* 
                                    FROM instructors i JOIN schools s on i.school_id=s.id
                                    JOIN courses c on c.instructor_id=i.id
                                    WHERE s.id=%s AND c.is_monitored=TRUE;'''
        params = (school_config.SCHOOL_ID,)
        instructors = db.run_query(INSTRUCTORS_QUERY, cursor, params)

        logger.info(f'{len(instructors)} instructors found in db with active course instance')
        for i in instructors:
            logger.info(f"Processing instructor {i['first_name']} {i['last_name']}")
            # Connect to the instructors LMS using their API token
            lms_token = i['lms_token']
            lms_obj = LmsClass(lms_token, school_config.API_BASE_URL)

            # Create the instructor object from db info and grab all their courses from db
            instructor = Instructor(first_name=i['first_name'],
                                    last_name=i['last_name'],
                                    email=i['email'],
                                    lms_id=i['lms_id'],
                                    color_blind_mode=i['color_blind_mode'])
            INSTRUCTOR_COURSES = f'''SELECT DISTINCT lms_id, short_name, alias
                                     FROM courses
                                     WHERE instructor_id = %s AND is_monitored=TRUE'''
            params = (i['id'],)
            instructor_courses_dict = db.run_query(INSTRUCTOR_COURSES, cursor, params)
            instructor.add_courses([Course(lms_id=c['lms_id'],
                                           short_name=c['short_name'],
                                           alias=c['alias']) for c in instructor_courses_dict])

            for course in instructor.courses:
                logger.info(f'Getting grades/assignments for {course.short_name}...')
                # Get the students, enrollments, assigments, and grades for this course
                students_dict = lms_obj.get_students_in_course(course.lms_id)
                if students_dict is None:
                    continue
                students = [Student(name=student['name'], lms_id=student['lms_id']) for student in students_dict]
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
                                              course,
                                              datetime_format=school_config.DATETIME_FORMAT) for assignment in assignments_dict]
                course.add_assignments(assignments)

                # Get grades for all assignments, arranged by student
                grades_dict = lms_obj.get_course_grades(course.lms_id, students)
                # Get overall grades for all students (cumulative grade)
                current_scores_dict = lms_obj.get_current_scores(course.lms_id)
                # Create an Enrollment object for each student with all of their assignments,
                # along with their current grade
                for student in course.students:
                    enrollment = Enrollment(student, course, current_score=current_scores_dict.get(student.lms_id))
                    student_grades = []
                    for assignment in assignments:
                        # Find the entry in grades_dict corresponding to this assignment
                        assignment_score = [s for s in grades_dict.get(str(student.lms_id), [])
                                            if str(s['lms_id']) == str(assignment.lms_id)]
                        if assignment_score:
                            student_grades.append(Grade(student, course, assignment, assignment_score[0].get('score')))
                    enrollment.add_grades(student_grades)
                    student.add_enrollments(enrollment)

            # Context dictionaries are used by Jinja to create the emails
            course_context_dicts = []
            for course in instructor.courses:
                logger.info(f'Finding outliers for {course.short_name}...')
                course_outliers = defaultdict(list)
                for student in course.students:
                    # Create CI's for each student -> floats
                    enrollment = student.get_enrollment_by_course(course)

                    # Look for new good/bad results -> Assignments
                    if ref_date is not None:
                        enrollment.form_ci(ref_date=ref_date, distribution=school_config.DISTRIBUTION)
                        outlier_assignments = enrollment.get_outliers(ref_date=ref_date)
                    else:
                        enrollment.form_ci(distribution=school_config.DISTRIBUTION)
                        outlier_assignments = enrollment.get_outliers()

                    # Create student summary -> list of Assignments
                    if outlier_assignments:
                        course_outliers[enrollment] = outlier_assignments
                        if school_config.COMMIT_OUTLIERS_TO_DB:
                            enrollment.commit_outliers_to_db(outlier_assignments, cursor, conn)

                # Create class summary (mean/median class grade)
                summary_stat = school_config.COURSE_SUMMARY_STAT
                summary_stat_value = lms_obj.get_course_grade_summary(course.lms_id, summary_stat)
                course_summary = {'summary_stat': summary_stat, 'summary_stat_value': summary_stat_value}

                # Craft (email) card for this course
                course_card = course.context_dict(course_outliers, course_summary)
                course_context_dicts.append(course_card)

            # Send email
            context_dict = {'context_dicts': course_context_dicts,
                            'instructor': instructor,
                            'current_date': datetime.datetime.now() - datetime.timedelta(days=1),
                            'week_start': datetime.datetime.now() - datetime.timedelta(days=8)
                            }
            jinja_env = prep_jinja()
            email = instructor.render_email(context_dict, jinja_env)
            instructor.send_email(from_email=school_config.FROM_EMAIL, rendered_email=email)
            logger.info(f'{len(instructor.courses)} courses processed for instructor {instructor.email}')
