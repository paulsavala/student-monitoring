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

from collections import defaultdict
import datetime


class Dates:
    semester_first_sunday = datetime.datetime(2020, 1, 19)
    semester_last_sunday = datetime.datetime(2020, 5, 3)


if __name__ == '__main__':
    config = StEdwardsConfig

    # Bootstrap if needed and get the connection and a cursor
    conn, cursor = bootstrap(config, db)
    api_url = config.api_url

    ref_date = Dates.semester_last_sunday - datetime.timedelta(weeks=4)

    # Get the instructor
    INSTRUCTORS = '''SELECT * FROM instructors;'''
    instructors = db.run_query(INSTRUCTORS, cursor)
    for i in instructors:
        # Connect to the instructors Canvas account
        api_token = i['api_token']
        lms = config.load_lms(api_url, api_token)
        instructor_dict = lms.get_instructor()
        instructor = Instructor(name=instructor_dict['name'],
                                email=instructor_dict['email'],
                                lms_id=instructor_dict['lms_id'])
        # INSTRUCTOR_COURSES = f'''SELECT DISTINCT course FROM course_instances WHERE instructor=?'''
        # params = (instructor['lms_id'])
        # instructor_courses_dict = db.run_query(INSTRUCTOR_COURSES, cursor, params)
        # instructor.add_courses([Course(instructor_courses_dict[''])])
        courses_dict = lms.get_courses_by_instructor(instructor, config.semester)
        instructor.add_courses([Course(c['id'], c['name']) for c in courses_dict])

        for course in instructor.courses:
            # Get the students, enrollments, assigments, and grades for this course
            students_dict = lms.get_students_in_course(course)
            students = [Student(student['name'],
                                student['lms_id']) for student in students_dict]
            course.add_students(students)

            assignments_dict = lms.get_course_assignments(course)
            # Check to make sure the course actually has assignments (for example, 4157 should be skipped)
            if not assignments_dict:
                assignments = []
            else:
                assignments = [Assignment(assignment['lms_id'],
                                          assignment['name'],
                                          assignment['due_date'],
                                          course) for assignment in assignments_dict]
            course.add_assignments(assignments)

            grades_dict = lms.get_course_grades(course, students, assignments)
            current_scores_dict = lms.get_current_scores(course)
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
                enrollment.form_ci(distribution=config.distribution)

                # Look for new good/bad results -> Assignments
                outlier_assignments = enrollment.get_outliers(ref_date=ref_date)

                # Create student summary -> list of Assignments
                if outlier_assignments:
                    course_outliers[enrollment] = outlier_assignments
                    if config.commit_outliers_to_db:
                        enrollment.commit_outliers_to_db(outlier_assignments, cursor, conn)

            # Create class summary (mean/median class grade)
            summary_stat = config.course_summary_stat
            summary_stat_value = lms.get_course_grade_summary(course, summary_stat=summary_stat)
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
