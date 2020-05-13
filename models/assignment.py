from datetime import datetime


class Assignment:
    def __init__(self, student, assigment_name, due_date, score):
        self.student = student
        self.assigment_name = assigment_name
        self.due_date = due_date
        self.score = score

        if isinstance(due_date, str):
            # todo: How can I pull this from the config instead? Don't want to pass the config due to circular imports,
            # todo: and I want this to work for any config.
            self.due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%SZ')

    def is_outlier(self, left, right):
        is_outlier = (self.score < left) or (self.score > right)
        return is_outlier


class AssignmentCollection:
    def __init__(self, student, course, assignments):
        self.student = student
        self.course = course
        self.assignments = assignments

    def get_grades(self, current_week=False, return_assignments=False, ref_date=None):
        """
        Returns the grades (as a float between 0 and 1 inclusive)
        :param: current_week: (Bool) Whether to return all grades for only the past seven days, or for the
                                entire semester. Defaults to False.
        :param: return_assignments: (Bool) Whether or not to return the entire assignment or just the grade (score).
                                    Defaults to False.
        :param: ref_date: (date or datetime)
        :return: List of floats (grades)
        """
        if not current_week:
            grades = [a for a in self.assignments]
        else:
            if ref_date is None:
                ref_date = datetime.now()
            grades = [a for a in self.assignments if (ref_date - a.due_date).days <= 7]
        if not return_assignments:
            grades = [a.score for a in grades]
        return grades

    def form_ci(self, distribution, conf_level=0.05, default_left=0.7, default_right=1):
        d = distribution(default_left=default_left, default_right=default_right)
        all_grades = self.get_grades()
        d.fit(all_grades)
        left, right = d.conf_int(conf_level)
        return left, right

    def update_assignment_student(self, student):
        self.student = student
        for a in self.assignments:
            a.student = student

    # def identify_outliers(self, left, right, ref_date=None):
    #     current_assignments = self.get_grades(current_week=True, return_assignments=True, ref_date=ref_date)
    #     outlier_assignments = [a for a in current_assignments if a.is_outlier(left, right)]
    #     # outliers = AssignmentCollection(self.student, self.course, outlier_assignments)
    #     return outlier_assignments
