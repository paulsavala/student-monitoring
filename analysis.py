from config import StEdwardsConfig
from utils import db
from bootstrap.db import bootstrap

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
        ref_date = datetime.datetime(2020, 4, 5)
        for course in instructor.courses:
            course_outliers = defaultdict(list)
            for student in course.students:
                # Create CI's for each student -> floats
                student.form_ci(course, config.distribution, save_ci=True)

                # Look for new good/bad results -> Assignments
                outlier_assignments = student.get_outliers(course, ref_date=ref_date)

                # Create student summary -> list of Assignments
                if outlier_assignments:
                    course_outliers[student] = outlier_assignments

            # Create class summary (mean/median class grade)
            summary_stat = config.course_summary_stat
            summary_stat_value = lms.get_course_grade_summary(course, summary_stat=summary_stat)
            course_summary = {'summary_stat': summary_stat, 'summary_stat_value': summary_stat_value}

            # Run analysis
