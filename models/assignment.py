

class Assignment:
    def __init__(self, student, assigment_name, due_date, score):
        self.student = student
        self.assigment_name = assigment_name
        self.due_date = due_date
        self.score = score


class AssignmentCollection:
    def __init__(self, student, course, assignments):
        self.student = student
        self.course = course
        self.assignments = assignments

    def get_grades(self, week=None):
        """
        Returns the grades (as a float between 0 and 1 inclusive)
        :param: week: The week (as an int indicating the week number) for which to grab grades. Leave as None if you
                        you want all grades.
        :return: List of floats (grades)
        """
        if week is None:
            grades = [a.score for a in self.assignments]
        else:
            raise NotImplementedError
            # grades = [a.score for a in self.assignments if ]

    def form_ci(self, distribution, level=0.05):
        d = distribution()
        grades = self.get_grades()
        d.fit(grades)
        left, right = d.conf_int()
        self.identify_outliers(left, right)
        raise NotImplementedError

    def identify_outliers(self, left, right):
        raise NotImplementedError
