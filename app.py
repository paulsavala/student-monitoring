from config import StEdwardsConfig
from utils import db
import os

from models.instructor import Instructor


def bootstrap():
    if not os.path.exists(StEdwardsConfig.db_file):
        # Create an empty db file
        with open(StEdwardsConfig.db_file, 'w') as f:
            pass

    conn = db.create_connection(StEdwardsConfig.db_file)
    cursor = db.create_cursor(conn)

    CREATE_INSTRUCTOR_TABLE = '''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            api_token TEXT NOT NULL
        );
        '''
    CREATE_COURSE_TABLE = '''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                department TEXT NOT NULL,
                number INTEGER NOT NULL,
                section INTEGER,
                canvas_id INTEGER
            );
            '''
    db.run_query(CREATE_INSTRUCTOR_TABLE, cursor)
    db.run_query(CREATE_COURSE_TABLE, cursor)

    CREATE_INITIAL_INSTRUCTOR = '''
        INSERT INTO instructors (first_name, last_name, email, department, api_token) 
        SELECT 'Paul', 'Savala', 'psavala@stedwards.edu', 'MATH', '3286~8dlESHq3nIk4XSxU43srFlqhCJbQFxHD1rwFYhx6mo2A1oXB7INfi94csvP4NuWX'
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


if __name__ == '__main__':
    # Bootstrap if needed and get the connection and a cursor
    conn, cursor = bootstrap()
    api_url = 'https://stedwards.instructure.com/'

    # Get the instructor
    INSTRUCTORS = '''SELECT * FROM instructors;'''
    instructors = db.run_query(INSTRUCTORS, cursor)
    for i in instructors:
        # Connect to the instructors Canvas account
        api_token = i['api_token']
        lms = StEdwardsConfig.lms(api_token, api_url)
        instructor = Instructor(i['first_name'], i['last_name'], i['email'])

        # Fetch the instructor's courses
        courses = instructor.get_courses()

        for c in courses:
            # Fetch the students in each course
            students = c.get_students()

            for s in students:
                # Fetch the grades for those students
                grades = s.get_grades(c)

                # Create CI's for each student
                grades.form_ci()

                # Look for new good/bad results
                grades.identify_outliers()

                # Create student summary
                s.set_grades(grades)
                s.create_summary()

            # (Optional) Create class summary
            c.create_summary()

            # Craft email
            c.create_email()

        # Send email
        pass
