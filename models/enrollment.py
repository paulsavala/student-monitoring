from utils.models import add_to_list, remove_from_list
from utils.db import run_query

from datetime import datetime
from logzero import logger


class Enrollment:
    def __init__(self, student, course, grades=None, current_score=None, ci_left=None, ci_right=None):
        self.student = student
        self.course = course
        self.grades = grades
        self.current_score = current_score
        self.ci_left = ci_left
        self.ci_right = ci_right

    def add_grades(self, grades):
        self.grades = add_to_list(self.grades, grades)

    def remove_grades(self, grades):
        self.grades = remove_from_list(self.grades, grades)

    def get_grades(self, current_week=True, ref_date=None, scores_only=False):
        if not current_week:
            if ref_date is None:
                grades = self.grades
            else:
                grades = [g for g in self.grades if g.assignment.due_date < ref_date]
        else:
            if ref_date is None:
                ref_date = datetime.now()
            grades = [g for g in self.grades
                      if (ref_date - g.assignment.due_date).days < 7 and g.assignment.due_date < ref_date]
        if scores_only:
            grades = [g.score for g in grades]
        return grades

    def form_ci(self, distribution, conf_level=0.1, default_left=0.7, default_right=1, save_ci=True, ref_date=None):
        d = distribution(default_left=default_left, default_right=default_right)
        all_grades = self.get_grades(current_week=False, ref_date=ref_date, scores_only=True)
        if len(all_grades) > 0:
            d.fit(all_grades)
            left, right = d.conf_int(conf_level)
            if save_ci:
                self.set_ci(left, right)
            return left, right
        else:
            logger.info(f'Student {self.student.name} has no grades for this time period, returning default CI')
            return default_left, default_right

    def set_ci(self, left, right):
        self.ci_left = left
        self.ci_right = right

    def get_outliers(self, ref_date=None):
        current_assignments = self.get_grades(ref_date=ref_date)
        outlier_assignments = [a for a in current_assignments if a.is_outlier(self.ci_left, self.ci_right)]
        return outlier_assignments

    def commit_outliers_to_db(self, outlier_assignments, cursor, conn):
        for assignment in outlier_assignments:
            COMMIT_QUERY = f'''
            INSERT INTO outliers (student_name, student_lms_id, assignment_name, course_lms_id, ci_left,
            ci_right, assignment_score, due_date)
            VALUES( ?, ?, ?, ?, ?, ?, ?, ?);
            '''
            params = (self.name, str(self.lms_id), assignment.assignment_name, str(self.course.course_id), self.ci_left,
                      self.ci_right, assignment.score, assignment.due_date.strftime('%Y-%m-%d'))
            run_query(COMMIT_QUERY, cursor, params)
        conn.commit()
