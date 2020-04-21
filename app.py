from config import Config
from utils import db
import os


def bootstrap():
    if not os.path.exists(Config.db_file):
        # Create an empty db file
        with open(Config.db_file, 'w') as f:
            pass

    conn = db.create_connection(Config.db_file)
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
    api_token = '3286~8dlESHq3nIk4XSxU43srFlqhCJbQFxHD1rwFYhx6mo2A1oXB7INfi94csvP4NuWX'
    api_url = 'https://stedwards.instructure.com/'
    lms = Config.lms(api_token, api_url)

    # Fetch the instructor's courses

    # Fetch the students in each course

    # Fetch the grades for those students

    # Create CI's for each student

    # Look for new good/bad results

    # Create student summary

    # (Optional) Create class summary

    # Craft email

    # Send the email
    pass
