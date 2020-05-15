from datetime import datetime


class Student:
    def __init__(self, name, lms_id):
        self.name = name
        self.lms_id = lms_id

        self.assignments = dict()
        self.ci_left = None
        self.ci_right = None

    def set_assignments(self, course, assignments):
        if not isinstance(assignments, list):
            assignments = [assignments]
        self.assignments[course] = assignments

    def get_course_assignments(self, course, current_week=True, ref_date=None, scores_only=False):
        if not current_week:
            assignments = self.assignments.get(course)
        else:
            if ref_date is None:
                ref_date = datetime.now()
            assignments = [a for a in self.assignments.get(course)
                           if (ref_date - a.due_date).days < 7 and ref_date > a.due_date]
        if scores_only:
            assignments = [a.score for a in assignments]
        return assignments

    def form_ci(self, course, distribution, conf_level=0.1, default_left=0.7, default_right=1, save_ci=False):
        d = distribution(default_left=default_left, default_right=default_right)
        all_grades = self.get_course_assignments(course, scores_only=True, current_week=False)
        d.fit(all_grades)
        left, right = d.conf_int(conf_level)
        if save_ci:
            self.set_ci(left, right)
        return left, right

    def set_ci(self, left, right):
        self.ci_left = left
        self.ci_right = right

    def get_outliers(self, course, ref_date=None):
        current_assignments = self.get_course_assignments(course,
                                                          ref_date=ref_date)
        outlier_assignments = [a for a in current_assignments if a.is_outlier(self.ci_left, self.ci_right)]
        return outlier_assignments
