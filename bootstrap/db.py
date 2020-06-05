import os


def bootstrap(config, db):
    if not os.path.exists(config.db_file):
        # Create an empty db file
        with open(config.db_file, 'w'):
            pass

    conn = db.create_connection(config.db_file)
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
    CREATE_COURSE_INSTANCE_TABLE = '''
                CREATE TABLE IF NOT EXISTS course_instances (
                    id INTEGER PRIMARY KEY,
                    instructor INTEGER NOT NULL,
                    course INTEGER NOT NULL,
                    season VARCHAR(128),
                    year INTEGER,
                    FOREIGN KEY (instructor) REFERENCES instructors(id),
                    FOREIGN KEY (course) REFERENCES courses(id)
                );
                '''
    CREATE_OUTLIERS_TABLE = '''
                CREATE TABLE IF NOT EXISTS outliers (
                    id INTEGER PRIMARY KEY,
                    student_name VARCHAR(128) NOT NULL,
                    student_lms_id VARCHAR(128) NOT NULL,
                    assignment_name VARCHAR(128) NOT NULL,
                    course_lms_id VARCHAR(128) NOT NULL,
                    ci_left FLOAT NOT NULL,
                    ci_right FLOAT NOT NULL,
                    assignment_score FLOAT NOT NULL,
                    due_date TIMESTAMP NOT NULL
                );
                '''
    db.run_query(CREATE_INSTRUCTOR_TABLE, cursor)
    db.run_query(CREATE_COURSE_TABLE, cursor)
    db.run_query(CREATE_COURSE_INSTANCE_TABLE, cursor)
    db.run_query(CREATE_OUTLIERS_TABLE, cursor)

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
    CREATE_SECOND_COURSE = '''
            INSERT INTO courses (department, number, section, canvas_id) 
            SELECT 'MATH', 3320, 1, 21853
            WHERE NOT EXISTS (SELECT 1 FROM courses WHERE canvas_id = 21853);
        '''
    CREATE_THIRD_COURSE = '''
            INSERT INTO courses (department, number, section, canvas_id) 
            SELECT 'MATH', 3349, 1, 12345
            WHERE NOT EXISTS (SELECT 1 FROM courses WHERE canvas_id = 12345);
        '''
    CREATE_INITIAL_COURSE_INSTANCE = '''
            INSERT INTO course_instances (instructor, course, season, year) 
            VALUES ((SELECT id FROM instructors WHERE email='psavala@stedwards.edu'), 
            (SELECT id FROM courses WHERE department='MATH' and number=3320 and section=2),
            'SPRING', 2020);
        '''
    CREATE_SECOND_COURSE_INSTANCE = '''
                INSERT INTO course_instances (instructor, course, season, year) 
                VALUES ((SELECT id FROM instructors WHERE email='psavala@stedwards.edu'), 
                (SELECT id FROM courses WHERE department='MATH' and number=3320 and section=1),
                'SPRING', 2020);
            '''
    CREATE_THIRD_COURSE_INSTANCE = '''
                INSERT INTO course_instances (instructor, course, season, year) 
                VALUES ((SELECT id FROM instructors WHERE email='psavala@stedwards.edu'), 
                (SELECT id FROM courses WHERE department='MATH' and number=3349 and section=1),
                'SPRING', 2020);
            '''
    db.run_query(CREATE_INITIAL_INSTRUCTOR, cursor)
    db.run_query(CREATE_INITIAL_COURSE, cursor)
    db.run_query(CREATE_SECOND_COURSE, cursor)
    db.run_query(CREATE_THIRD_COURSE, cursor)
    db.run_query(CREATE_INITIAL_COURSE_INSTANCE, cursor)
    db.run_query(CREATE_SECOND_COURSE_INSTANCE, cursor)
    db.run_query(CREATE_THIRD_COURSE_INSTANCE, cursor)

    conn.commit()

    return conn, cursor
