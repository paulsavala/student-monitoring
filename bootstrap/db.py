from logzero import logger


def bootstrap(config, db):
    logger.info('Starting bootstrapping db...')
    conn = db.create_connection(config.DB_ENDPOINT)
    cursor = db.create_cursor(conn)


    CREATE_SCHOOL_TABLE = '''
        CREATE TABLE IF NOT EXISTS schools (
            id INTEGER PRIMARY KEY,
            name VARCHAR(256) NOT NULL,
            city VARCHAR(128) NOT NULL,
            state VARCHAR(2) NOT NULL,
            api_url VARCHAR(256)
        );
    '''
    CREATE_COLLEGE_OF_TABLE = '''
        CREATE TABLE IF NOT EXISTS college_of (
            id INTEGER PRIMARY KEY,
            long_name VARCHAR(128),
            short_name VARCHAR(16), 
            
            school_id INTEGER NOT NULL,
            FOREIGN KEY (school_id) REFERENCES schools(id)
        );
    '''
    CREATE_DEPARTMENT_TABLE = '''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            long_name VARCHAR(256) NOT NULL,
            short_name VARCHAR(16) NOT NULL UNIQUE,
            
            school_id INTEGER NOT NULL,
            college_of_id INTEGER NOT NULL,
            FOREIGN KEY (school_id) REFERENCES schools(id),
            FOREIGN KEY (college_of_id) REFERENCES college_of(id)
        );
    '''
    CREATE_INSTRUCTOR_TABLE = '''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY,
            first_name VARCHAR(64),
            last_name VARCHAR(64),
            email VARCHAR(128) UNIQUE,
            lms_id VARCHAR(1024),
            lms_token VARCHAR(128),
            is_admin BOOLEAN DEFAULT FALSE,
            is_registered BOOLEAN DEFAULT FALSE,
            
            department_id INTEGER,
            school_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (school_id) REFERENCES schools(id)
        );
        '''
    CREATE_COURSE_TABLE = '''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name VARCHAR(256),
                department_short_name VARCHAR(16),
                number INTEGER NOT NULL,
                
                department_id INTEGER NOT NULL,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            );
            '''
    CREATE_COURSE_INSTANCE_TABLE = '''
                CREATE TABLE IF NOT EXISTS course_instances (
                    id INTEGER PRIMARY KEY,
                    lms_id VARCHAR(1024) UNIQUE,
                    season VARCHAR(64),
                    year INTEGER,
                    section VARCHAR(64),
                    auto_email BOOLEAN DEFAULT FALSE,
                    
                    course_id INTEGER NOT NULL,
                    instructor_id INTEGER,
                    department_id INTEGER NOT NULL,
                    FOREIGN KEY (course_id) REFERENCES courses(id),
                    FOREIGN KEY (instructor_id) REFERENCES instructors(id),
                    FOREIGN KEY (department_id) REFERENCES departments(id)
                );
                '''
    CREATE_OUTLIERS_TABLE = '''
                CREATE TABLE IF NOT EXISTS outliers (
                    id INTEGER PRIMARY KEY,
                    student_id VARCHAR(128),
                    assignment_name VARCHAR(128),
                    course_lms_id VARCHAR(128) NOT NULL,
                    ci_left FLOAT NOT NULL,
                    ci_right FLOAT NOT NULL,
                    assignment_score FLOAT NOT NULL,
                    due_date TIMESTAMP
                );
                '''
    db.run_query(CREATE_SCHOOL_TABLE, cursor)
    db.run_query(CREATE_COLLEGE_OF_TABLE, cursor)
    db.run_query(CREATE_DEPARTMENT_TABLE, cursor)
    db.run_query(CREATE_INSTRUCTOR_TABLE, cursor)
    db.run_query(CREATE_COURSE_TABLE, cursor)
    db.run_query(CREATE_COURSE_INSTANCE_TABLE, cursor)
    db.run_query(CREATE_OUTLIERS_TABLE, cursor)

    CREATE_INITIAL_SCHOOL = '''
        INSERT INTO schools (id, name, city, state, api_url)
        SELECT 1, 'ST EDWARDS UNIVERSITY', 'AUSTIN', 'TX', 'https://stedwards.instructure.com/'
        WHERE NOT EXISTS (SELECT 1 FROM schools WHERE name='ST EDWARDS UNIVERSITY');
    '''
    CREATE_INITIAL_NSCI = '''
            INSERT INTO college_of (id, long_name, short_name, school_id)
            SELECT 1, 'SCHOOL OF NATURAL SCIENCES', 'NSCI', 1
            WHERE NOT EXISTS (SELECT 1 FROM college_of WHERE long_name='SCHOOL OF NATURAL SCIENCES' and school_id=1);
        '''
    CREATE_MATH_DEPARTMENT = '''
            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
            SELECT 'MATHEMATICS', 'MATH', 1, 1
            WHERE NOT EXISTS (SELECT 1 FROM departments WHERE short_name='MATH' AND school_id=1);
        '''
    CREATE_CS_DEPARTMENT = '''
                INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                SELECT 'COMPUTER SCIENCE', 'CS', 1, 1
                WHERE NOT EXISTS (SELECT 1 FROM departments WHERE short_name='CS' AND school_id=1);
            '''

    db.run_query(CREATE_INITIAL_SCHOOL, cursor)
    db.run_query(CREATE_INITIAL_NSCI, cursor)
    db.run_query(CREATE_MATH_DEPARTMENT, cursor)
    db.run_query(CREATE_CS_DEPARTMENT, cursor)
    conn.commit()
    logger.info('Database bootstrapped')

    return conn, cursor
