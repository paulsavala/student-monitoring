import os


def bootstrap(config, db):
    if not os.path.exists(config.db_file):
        # Create an empty db file
        with open(config.db_file, 'w'):
            pass

    conn = db.create_connection(config.db_file)
    cursor = db.create_cursor(conn)

    CREATE_SCHOOL_TABLE = '''
        CREATE TABLE IF NOT EXISTS schools (
            id INTEGER PRIMARY KEY,
            name VARCHAR(256) NOT NULL,
            city VARCHAR(128) NOT NULL,
            state VARCHAR(2) NOT NULL
        );
    '''
    CREATE_DEPARTMENT_TABLE = '''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            long_name VARCHAR(256) NOT NULL,
            short_name VARCHAR(16) NOT NULL UNIQUE,
            college VARCHAR(128),
            school INTEGER NOT NULL,
            FOREIGN KEY (school) REFERENCES schools(id)
        );
    '''
    # instructor.id is a varchar to support flask_login, which requires this
    CREATE_INSTRUCTOR_TABLE = '''
        CREATE TABLE IF NOT EXISTS instructors (
            id VARCHAR(256) PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            email VARCHAR(128) NOT NULL UNIQUE,
            department VARCHAR(128),
            profile_pic VARCHAR(256),
            api_token VARCHAR(128),
            is_admin BOOLEAN DEFAULT FALSE
        );
        '''
    CREATE_COURSE_TABLE = '''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name VARCHAR(256) NOT NULL,
                department VARCHAR(128) NOT NULL,
                number INTEGER NOT NULL
            );
            '''
    CREATE_COURSE_INSTANCE_TABLE = '''
                CREATE TABLE IF NOT EXISTS course_instances (
                    id INTEGER PRIMARY KEY,
                    canvas_id INTEGER,
                    instructor INTEGER NOT NULL,
                    course INTEGER NOT NULL,
                    season VARCHAR(128),
                    year INTEGER,
                    section INTEGER,
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
    db.run_query(CREATE_SCHOOL_TABLE, cursor)
    db.run_query(CREATE_DEPARTMENT_TABLE, cursor)
    db.run_query(CREATE_INSTRUCTOR_TABLE, cursor)
    db.run_query(CREATE_COURSE_TABLE, cursor)
    db.run_query(CREATE_COURSE_INSTANCE_TABLE, cursor)
    db.run_query(CREATE_OUTLIERS_TABLE, cursor)

    CREATE_INITIAL_SCHOOL = '''
        INSERT INTO schools (name, city, state)
        SELECT "ST. EDWARD'S UNIVERSITY", 'AUSTIN', 'TX'
        WHERE NOT EXISTS (SELECT 1 FROM schools WHERE name="ST. EDWARD'S UNIVERSITY");
    '''
    CREATE_MATH_DEPARTMENT = '''
            INSERT INTO departments (long_name, short_name, college, school)
            SELECT "MATHEMATICS", 'MATH', 'NATURAL SCIENCE', 1
            WHERE NOT EXISTS (SELECT 1 FROM departments WHERE short_name="MATH");
        '''
    CREATE_CS_DEPARTMENT = '''
                INSERT INTO departments (long_name, short_name, college, school)
                SELECT "COMPUTER SCIENCE", 'CSCI', 'NATURAL SCIENCE', 1
                WHERE NOT EXISTS (SELECT 1 FROM departments WHERE short_name="CSCI");
            '''
    CREATE_BIOLOGY_DEPARTMENT = '''
                    INSERT INTO departments (long_name, short_name, college, school)
                    SELECT "BIOLOGY", 'BIO', 'NATURAL SCIENCE', 1
                    WHERE NOT EXISTS (SELECT 1 FROM departments WHERE short_name="BIO");
                '''

    db.run_query(CREATE_INITIAL_SCHOOL, cursor)
    db.run_query(CREATE_MATH_DEPARTMENT, cursor)
    db.run_query(CREATE_CS_DEPARTMENT, cursor)
    db.run_query(CREATE_BIOLOGY_DEPARTMENT, cursor)
    conn.commit()

    return conn, cursor
