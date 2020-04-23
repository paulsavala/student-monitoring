from config import StEdwardsConfig
from utils import db
import os


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

        for course in instructor.courses:
            for student in course.students:
                # Fetch the grades for those students
                assignments = student.get_course_assignments(course)

                # Create CI's for each student
                left, right = assignments.form_ci(StEdwardsConfig.distribution)

                # Look for new good/bad results
                outlier_assignments = assignments.identify_outliers(left, right)

                # Create student summary
                student.create_summary(outlier_assignments)

            # (Optional) Create class summary
            course.create_summary()

            # Craft email
            course.create_email()

        # Send email
        instructor.send_email()
