from config import StEdwardsConfig
from utils import db
from bootstrap.db import bootstrap

from collections import defaultdict
import datetime
import pandas as pd


class Dates:
    semester_first_sunday = datetime.datetime(2020, 1, 19)
    semester_last_sunday = datetime.datetime(2020, 5, 3)


class CourseAnalysis:
    def __init__(self, course):
        self.course = course
        self.course_outliers = None
        self.results_dict = defaultdict(list)

    def summarize_results(self, ref_date):
        for student, outlier_assignments in self.course_outliers.items():
            self.results_dict['name'].append(student.name)
            self.results_dict['id'].append(student.lms_id)
            self.results_dict['week'].append(ref_date)
            self.results_dict['final_grade'].append(student.current_score[self.course])

            low_outliers = [a for a in outlier_assignments if a.score < student.ci_left]
            high_outliers = [a for a in outlier_assignments if a.score > student.ci_right]

            self.results_dict['num_low_outliers'].append(len(low_outliers))
            self.results_dict['num_high_outliers'].append(len(high_outliers))

    def save_results(self):
        results_df = pd.DataFrame(self.results_dict)
        results_df.to_csv(f'{course.name}_{datetime.date.today().strftime("%Y_%m_%d")}_analysis.csv', index=False)


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

        # Used for testing since there are no current assignments
        ref_date = Dates.semester_first_sunday
        for course in instructor.courses:
            # Used to store results for this course
            course_analysis = CourseAnalysis(course)
            while ref_date <= Dates.semester_last_sunday:
                course_outliers = defaultdict(list)
                for student in course.students:
                    # Create CI's for each student -> floats
                    student.form_ci(course, config.distribution, save_ci=True, ref_date=ref_date)

                    # Look for new good/bad results -> Assignments
                    outlier_assignments = student.get_outliers(course, ref_date=ref_date)

                    # Create student summary -> list of Assignments
                    if outlier_assignments:
                        course_outliers[student] = outlier_assignments
                        student.commit_outliers_to_db(outlier_assignments, course, cursor, conn)

                # Store results
                course_analysis.course_outliers = course_outliers
                course_analysis.summarize_results(ref_date)
                ref_date += datetime.timedelta(weeks=1)
            course_analysis.save_results()
            ref_date = Dates.semester_first_sunday

