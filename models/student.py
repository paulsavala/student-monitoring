

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

    def get_course_assignments(self, course):
        course_assignments = self.assignments.get(course)
        return course_assignments

    def form_ci(self, course, distribution, conf_level=0.05, default_left=0.7, default_right=1):
        d = distribution(default_left=default_left, default_right=default_right)
        all_grades = self.get_course_assignments(course)
        d.fit(all_grades)
        left, right = d.conf_int(conf_level)
        return left, right

    def set_ci(self, left, right):
        self.ci_left = left
        self.ci_right = right

    def get_outliers(self, course, ref_date=None):
        course_assignments = self.get_course_assignments(course)
        current_assignments = course_assignments.get_grades(current_week=True,
                                                            return_assignments=True,
                                                            ref_date=ref_date)
        outlier_assignments = [a for a in current_assignments if a.is_outlier(self.ci_left, self.ci_right)]
        return outlier_assignments
