from datetime import datetime

from utils.db import run_query
from utils.models import add_to_list, remove_from_list


class Student:
    def __init__(self, name, lms_id, enrollments=None):
        self.name = name
        self.lms_id = lms_id
        self.enrollments = enrollments

    def add_enrollments(self, enrollments):
        self.enrollments = add_to_list(self.enrollments, enrollments)

    def remove_enrollments(self, enrollments):
        self.enrollments = remove_from_list(self.enrollments, enrollments)

    def set_current_score(self, course, current_score):
        self.current_score[course] = current_score

    def set_assignments(self, course, assignments):
        if not isinstance(assignments, list):
            assignments = [assignments]
        self.assignments[course] = assignments

    def get_course_assignments(self, course, current_week=True, ref_date=None, scores_only=False):
        if not current_week:
            if ref_date is None:
                assignments = self.assignments.get(course)
            else:
                assignments = [a for a in self.assignments.get(course) if a.due_date < ref_date]
        else:
            if ref_date is None:
                ref_date = datetime.now()
            assignments = [a for a in self.assignments.get(course)
                           if (ref_date - a.due_date).days < 7 and a.due_date < ref_date]
        if scores_only:
            assignments = [a.score for a in assignments]
        return assignments

    def form_ci(self, course, distribution, conf_level=0.1, default_left=0.7, default_right=1, save_ci=False,
                ref_date=None):
        d = distribution(default_left=default_left, default_right=default_right)
        all_grades = self.get_course_assignments(course, scores_only=True, current_week=False, ref_date=ref_date)
        d.fit(all_grades)
        left, right = d.conf_int(conf_level)
        if save_ci:
            self.set_ci(left, right)
        return left, right

    def set_ci(self, left, right):
        self.ci_left = left
        self.ci_right = right

    def get_outliers(self, course, ref_date=None):
        current_assignments = self.get_course_assignments(course, ref_date=ref_date)
        outlier_assignments = [a for a in current_assignments if a.is_outlier(self.ci_left, self.ci_right)]
        return outlier_assignments

    def commit_outliers_to_db(self, outlier_assignments, course, cursor, conn):
        for assignment in outlier_assignments:
            COMMIT_QUERY = f'''
            INSERT INTO outliers (student_name, student_lms_id, assignment_name, course_lms_id, ci_left,
            ci_right, assignment_score, due_date)
            VALUES( ?, ?, ?, ?, ?, ?, ?, ?);
            '''
            params = (self.name, str(self.lms_id), assignment.assignment_name, str(course.course_id), self.ci_left,
                      self.ci_right, assignment.score, assignment.due_date.strftime('%Y-%m-%d'))
            run_query(COMMIT_QUERY, cursor, params)
        conn.commit()
