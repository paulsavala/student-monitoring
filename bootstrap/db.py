from logzero import logger
import os


def bootstrap(db_endpoint, db):
    conn = db.create_connection(db_endpoint)
    cursor = db.create_cursor(conn)

    if os.environ.get('BOOTSTRAP_DB'):
        logger.info('Bootstrapping database...')
        CREATE_SCHOOL_TABLE = '''
            CREATE TABLE IF NOT EXISTS schools (
                id SERIAL PRIMARY KEY,
                name VARCHAR(256) NOT NULL,
                city VARCHAR(128) NOT NULL,
                state VARCHAR(2) NOT NULL,
                api_url VARCHAR(256),
                config_class_name VARCHAR(256)
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
                short_name VARCHAR(16) NOT NULL,
                
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
            INSERT INTO schools (id, name, city, state, api_url, config_class_name)
            VALUES (1, 'St Edwards University', 'Austin', 'TX', 'https://stedwards.instructure.com/', 'StEdwardsConfig');
        '''

        # NSCI
        CREATE_INITIAL_NSCI = '''
                INSERT INTO college_of (id, long_name, short_name, school_id)
                VALUES (1, 'School of Natural Sciences', 'NSCI', 1);
            '''
        CREATE_MATH_DEPARTMENT = '''
                INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                VALUES ('Mathematics', 'MATH', 1, 1);
            '''
        CREATE_CS_DEPARTMENT = '''
                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                    VALUES ('Computer Science', 'COSC', 1, 1);
                '''
        CREATE_CHEM_DEPARTMENT = '''
                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                            VALUES ('Chemistry', 'CHEM', 1, 1);
                        '''
        CREATE_FORENSIC_SCIENCE_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Forensic Science', 'FRSC', 1, 1);
                                '''

        # Arts and humanities
        CREATE_INITIAL_ARTS_HUMANITIES = '''
                        INSERT INTO college_of (id, long_name, short_name, school_id)
                        VALUES (2, 'School of Arts and Humanities', 'HUM', 1);
                    '''
        CREATE_COMM_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Communication', 'COMM', 2, 1);
                                '''
        CREATE_LANGUAGES_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Languages, Literatures and Cultures', 'LLC', 2, 1);
                                        '''
        CREATE_LIT_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Literature, Writing and Rhetoric', 'LWR', 2, 1);
                                        '''
        CREATE_PERFORMING_ARTS_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Performing Arts', 'PA', 2, 1);
                                        '''
        CREATE_PHIL_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Philosophy', 'PHIL', 2, 1);
                                        '''
        CREATE_RELIGIOUS_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Religious and Theological Studies', 'RTS', 2, 1);
                                        '''
        CREATE_VISUAL_STUDIES_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Visual Studies', 'VS', 2, 1);
                                        '''

        # Behavioral and Social Sciences
        CREATE_INITIAL_BEHAVIORAL_SS = '''
                                        INSERT INTO college_of (id, long_name, short_name, school_id)
                                        VALUES (3, 'School of Behavioral and Social Sciences', 'BSS', 1);
                                    '''
        CREATE_CRIM_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Criminal Justice', 'CRIM', 3, 1);
                                '''
        CREATE_SOCI_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Sociology and Social Work', 'SSW', 3, 1);
                                '''
        CREATE_HISTORY_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('History', 'HIST', 3, 1);
                                '''
        CREATE_POLISCI_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Political Science, Global Studies, Environmental Science and Policy', 'POLS', 3, 1);
                                '''
        CREATE_PSYCH_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Psychology and Behavioral Neuroscience', 'PSYC', 3, 1);
                                '''

        # BUSINESS
        CREATE_INITIAL_BUSINESS = '''
                                    INSERT INTO college_of (id, long_name, short_name, school_id)
                                    VALUES (4, 'Bill Munday School of Business', 'MSB', 1);
                                '''
        CREATE_ACCT_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Accounting', 'ACCT', 4, 1);
                                '''
        CREATE_FINANCE_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Finance and Economics', 'FIN', 4, 1);
                                        '''
        CREATE_MANAGEMENT_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Management', 'MANG', 4, 1);
                                        '''
        CREATE_MARKETING_DEPARTMENT = '''
                                            INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                            VALUES ('Marketing and Entrepreneurship', 'MARK', 4, 1);
                                        '''

        # GRADUATE AND PROFESSIONAL STUDIES
        CREATE_INITIAL_GRAD = '''
                                    INSERT INTO college_of (id, long_name, short_name, school_id)
                                    VALUES (5, 'Office of Graduate and Professional Studies', 'GPS', 1);
                                '''
        CREATE_TEACH_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Teaching, Learning, and Culture', 'TLC', 5, 1);
                                '''
        CREATE_COUNSELING_DEPARTMENT = '''
                                    INSERT INTO departments (long_name, short_name, college_of_id, school_id)
                                    VALUES ('Counseling and College Development', 'TLC', 5, 1);
                                '''

        # ST EDWARDS UNIVERSITY
        db.run_query(CREATE_INITIAL_SCHOOL, cursor)

        # NSCI
        db.run_query(CREATE_INITIAL_NSCI, cursor)
        db.run_query(CREATE_MATH_DEPARTMENT, cursor)
        db.run_query(CREATE_CS_DEPARTMENT, cursor)
        db.run_query(CREATE_CHEM_DEPARTMENT, cursor)
        db.run_query(CREATE_FORENSIC_SCIENCE_DEPARTMENT, cursor)

        # ARTS AND HUMANITIES
        db.run_query(CREATE_INITIAL_ARTS_HUMANITIES, cursor)
        db.run_query(CREATE_COMM_DEPARTMENT, cursor)
        db.run_query(CREATE_LANGUAGES_DEPARTMENT, cursor)
        db.run_query(CREATE_LIT_DEPARTMENT, cursor)
        db.run_query(CREATE_PERFORMING_ARTS_DEPARTMENT, cursor)
        db.run_query(CREATE_PHIL_DEPARTMENT, cursor)
        db.run_query(CREATE_RELIGIOUS_DEPARTMENT, cursor)
        db.run_query(CREATE_VISUAL_STUDIES_DEPARTMENT, cursor)

        # BEHAVIORAL AND SOCIAL SCIENCES
        db.run_query(CREATE_INITIAL_BEHAVIORAL_SS, cursor)
        db.run_query(CREATE_CRIM_DEPARTMENT, cursor)
        db.run_query(CREATE_SOCI_DEPARTMENT, cursor)
        db.run_query(CREATE_HISTORY_DEPARTMENT, cursor)
        db.run_query(CREATE_POLISCI_DEPARTMENT, cursor)
        db.run_query(CREATE_PSYCH_DEPARTMENT, cursor)

        # BUSINESS
        db.run_query(CREATE_INITIAL_BUSINESS, cursor)
        db.run_query(CREATE_ACCT_DEPARTMENT, cursor)
        db.run_query(CREATE_FINANCE_DEPARTMENT, cursor)
        db.run_query(CREATE_MANAGEMENT_DEPARTMENT, cursor)
        db.run_query(CREATE_MARKETING_DEPARTMENT, cursor)

        # GRADUATE AND PROFESSIONAL STUDIES
        db.run_query(CREATE_INITIAL_GRAD, cursor)
        db.run_query(CREATE_TEACH_DEPARTMENT, cursor)
        db.run_query(CREATE_COUNSELING_DEPARTMENT, cursor)

        conn.commit()
        logger.info('Database bootstrapped')

    return conn, cursor
