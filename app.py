from config import StEdwardsConfig
from utils import db
from bootstrap.db import bootstrap
from bootstrap.jinja import prep_jinja

from collections import defaultdict
import datetime


if __name__ == '__main__':
    config = StEdwardsConfig

    # Bootstrap if needed and get the connection and a cursor
    conn, cursor = bootstrap(config, db)
    api_url = config.api_url

    # Get the instructor
    INSTRUCTORS = '''SELECT * FROM instructors;'''
    instructors = db.run_query(INSTRUCTORS, cursor)
    for i in instructors:
        # Connect to the instructors Canvas account
        api_token = i['api_token']
        lms = config.load_lms(api_url, api_token)
        instructor = lms.get_instructor(populate=True)

        course_context_dicts = []
        # Used for testing since there are no current assignments
        for course in instructor.courses:
            course_outliers = defaultdict(list)
            for student in course.students:
                # Create CI's for each student -> floats
                student.form_ci(course, config.distribution, save_ci=True)

                # Look for new good/bad results -> Assignments
                outlier_assignments = student.get_outliers(course)

                # Create student summary -> list of Assignments
                if outlier_assignments:
                    course_outliers[student] = outlier_assignments
                    if config.commit_outliers_to_db:
                        student.commit_outliers_to_db(outlier_assignments, cursor, conn)

            # Create class summary (mean/median class grade)
            summary_stat = config.course_summary_stat
            summary_stat_value = lms.get_course_grade_summary(course, summary_stat=summary_stat)
            course_summary = {'summary_stat': summary_stat, 'summary_stat_value': summary_stat_value}

            # Craft (email) card for this course
            env = prep_jinja()
            course_card = course.context_dict(course_outliers, course_summary)
            course_context_dicts.append(course_card)

        # Send email
        context_dict = {'context_dicts': course_context_dicts,
                        'instructor': instructor,
                        'current_date': datetime.datetime.now(),
                        'week_start': datetime.datetime.now() - datetime.timedelta(days=6)
                        }
        email = instructor.render_email(context_dict, env)
        instructor.send_email(email)
