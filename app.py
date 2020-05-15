from config import StEdwardsConfig
from utils import db
import os
from collections import defaultdict
from datetime import datetime, date

from jinja2 import Environment, FileSystemLoader, select_autoescape


def bootstrap():
    if not os.path.exists(StEdwardsConfig.db_file):
        # Create an empty db file
        with open(StEdwardsConfig.db_file, 'w'):
            pass

    conn = db.create_connection(StEdwardsConfig.db_file)
    cursor = db.create_cursor(conn)

    CREATE_INSTRUCTOR_TABLE = '''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            email VARCHAR(128) NOT NULL UNIQUE,
            department VARCHAR(128) NOT NULL,
            api_token VARCHAR(128) NOT NULL
        );
        '''
    CREATE_COURSE_TABLE = '''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                department VARCHAR(128) NOT NULL,
                number INTEGER NOT NULL,
                section INTEGER,
                canvas_id INTEGER
            );
            '''
    db.run_query(CREATE_INSTRUCTOR_TABLE, cursor)
    db.run_query(CREATE_COURSE_TABLE, cursor)

    CREATE_INITIAL_INSTRUCTOR = '''
        INSERT INTO instructors (name, email, department, api_token) 
        SELECT 'Paul Savala', 'psavala@stedwards.edu', 'MATH', '3286~8dlESHq3nIk4XSxU43srFlqhCJbQFxHD1rwFYhx6mo2A1oXB7INfi94csvP4NuWX'
        WHERE NOT EXISTS (SELECT 1 FROM instructors WHERE email = 'psavala@stedwards.edu');
    '''
    CREATE_INITIAL_COURSE = '''
        INSERT INTO courses (department, number, section, canvas_id) 
        SELECT 'MATH', 3320, 2, 201832
        WHERE NOT EXISTS (SELECT 1 FROM courses WHERE canvas_id = 201832);
    '''
    db.run_query(CREATE_INITIAL_INSTRUCTOR, cursor)
    db.run_query(CREATE_INITIAL_COURSE, cursor)

    conn.commit()

    return conn, cursor


def prep_jinja():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )
    return env


if __name__ == '__main__':
    # Bootstrap if needed and get the connection and a cursor
    conn, cursor = bootstrap()
    api_url = StEdwardsConfig.api_url

    # Get the instructor
    INSTRUCTORS = '''SELECT * FROM instructors;'''
    instructors = db.run_query(INSTRUCTORS, cursor)
    for i in instructors:
        # Connect to the instructors Canvas account
        api_token = i['api_token']
        lms = StEdwardsConfig.load_lms(api_url, api_token)
        instructor = lms.get_instructor(populate=True)

        course_context_dicts = []
        # Used for testing since there are no current assignments
        ref_date = datetime(2020, 4, 5)
        for course in instructor.courses:
            course_outliers = defaultdict(list)
            for student in course.students:
                # Create CI's for each student -> floats
                student.form_ci(course, StEdwardsConfig.distribution, save_ci=True)

                # Look for new good/bad results -> Assignments
                outlier_assignments = student.get_outliers(course, ref_date=ref_date)

                # Create student summary -> list of Assignments
                if outlier_assignments:
                    course_outliers[student] = outlier_assignments

            # Create class summary (meam/median class grade)
            summary_stat = StEdwardsConfig.course_summary_stat
            summary_stat_value = lms.get_course_grade_summary(course, summary_stat=summary_stat)
            course_summary = {'summary_stat': summary_stat, 'summary_stat_value': summary_stat_value}

            # Craft (email) card for this course
            env = prep_jinja()
            course_card = course.context_dict(course_outliers, course_summary)
            course_context_dicts.append(course_card)

        # Send email
        context_dict = {'context_dicts': course_context_dicts,
                        'instructor': instructor,
                        'current_date': ref_date
                        }
        email = instructor.render_email(context_dict, env)
        instructor.send_email(email)
