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
