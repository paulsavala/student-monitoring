from datetime import datetime


class Assignment:
    def __init__(self, student, assigment_name, due_date, score):
        self.student = student
        self.assigment_name = assigment_name
        self.due_date = due_date
        self.score = score

        if isinstance(due_date, str):
            # todo: How can I pull this from the config instead? I don't want to pass the config, and I want
            # todo: this to work for any config.
            self.due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%SZ')


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
        :return: List of floats (grades)
        """
        if not current_week:
            grades = [a for a in self.assignments]
        else:
            if ref_date is None:
                ref_date = datetime.now()
            grades = [a for a in self.assignments if (ref_date - a.due_date).days < 8]
        if not return_assignments:
            grades = [a.score for a in grades]
        return grades

    def form_ci(self, distribution, conf_level=0.05):
        d = distribution()
        all_grades = self.get_grades()
        d.fit(all_grades)
        left, right = d.conf_int(conf_level)
        return left, right

    def identify_outliers(self, left, right, ref_date=None):
        current_assignments = self.get_grades(current_week=True, return_assignments=True, ref_date=ref_date)
        outlier_assignments = [a for a in current_assignments if a.score < left or a.score > right]
        outliers = AssignmentCollection(self.student, self.course, outlier_assignments)
        return outliers
