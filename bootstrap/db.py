from logzero import logger
import os


def bootstrap(config, db):
    logger.info('Starting bootstrapping db...')
    conn = db.create_connection(config.DB_ENDPOINT)
    cursor = db.create_cursor(conn)

    if os.environ.get('BOOTSTRAP_DB'):
        CREATE_SCHOOL_TABLE = '''
            CREATE TABLE IF NOT EXISTS schools (
                id SERIAL PRIMARY KEY,
                name VARCHAR(256) NOT NULL,
                city VARCHAR(128) NOT NULL,
                state VARCHAR(2) NOT NULL,
                api_url VARCHAR(256)
            );
        '''
        CREATE_COLLEGE_OF_TABLE = '''
            CREATE TABLE IF NOT EXISTS college_of (
                id SERIAL PRIMARY KEY,
                long_name VARCHAR(128),
                short_name VARCHAR(16), 
                
                school_id INTEGER NOT NULL,
                FOREIGN KEY (school_id) REFERENCES schools(id)
            );
        '''
        CREATE_DEPARTMENT_TABLE = '''
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
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
                id SERIAL PRIMARY KEY,
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
                    id SERIAL PRIMARY KEY,
                    lms_id VARCHAR(1024),
                    season VARCHAR(64),
                    year INTEGER,
                    short_name VARCHAR(64),
                    long_name VARCHAR(256),
                    is_monitored BOOLEAN DEFAULT FALSE,
                    auto_email BOOLEAN DEFAULT FALSE,
                    
                    instructor_id INTEGER,
                    FOREIGN KEY (instructor_id) REFERENCES instructors(id)
                );
                '''
        CREATE_OUTLIERS_TABLE = '''
                    CREATE TABLE IF NOT EXISTS outliers (
                        id SERIAL PRIMARY KEY,
                        student_id VARCHAR(128),
                        assignment_name VARCHAR(128),
                        ci_left FLOAT NOT NULL,
                        ci_right FLOAT NOT NULL,
                        assignment_score FLOAT NOT NULL,
                        due_date TIMESTAMP,
                        
                        course_id INTEGER,
                        FOREIGN KEY (course_id) REFERENCES courses(id)                       
                    );
                    '''
        db.run_query(CREATE_SCHOOL_TABLE, cursor)
        db.run_query(CREATE_COLLEGE_OF_TABLE, cursor)
        db.run_query(CREATE_DEPARTMENT_TABLE, cursor)
        db.run_query(CREATE_INSTRUCTOR_TABLE, cursor)
        db.run_query(CREATE_COURSE_TABLE, cursor)
        db.run_query(CREATE_OUTLIERS_TABLE, cursor)

        CREATE_INITIAL_SCHOOL = '''
            INSERT INTO schools (id, name, city, state, api_url)
            VALUES (1, 'ST EDWARDS UNIVERSITY', 'AUSTIN', 'TX', 'https://stedwards.instructure.com/');
        '''
        CREATE_INITIAL_NSCI = '''
                INSERT INTO college_of (id, long_name, short_name, school_id)
                VALUES (1, 'SCHOOL OF NATURAL SCIENCES', 'NSCI', 1);
            '''
        CREATE_MATH_DEPARTMENT = '''
                INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                VALUES ('MATHEMATICS', 'MATH', 1, 1);
            '''
        CREATE_CS_DEPARTMENT = '''
                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                    VALUES ('COMPUTER SCIENCE', 'CS', 1, 1);
                '''

        db.run_query(CREATE_INITIAL_SCHOOL, cursor)
        db.run_query(CREATE_INITIAL_NSCI, cursor)
        db.run_query(CREATE_MATH_DEPARTMENT, cursor)
        db.run_query(CREATE_CS_DEPARTMENT, cursor)
        conn.commit()
        logger.info('Database bootstrapped')

    return conn, cursor
