

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

    def form_ci(self, level=0.05):
        raise NotImplementedError

    def identify_outliers(self):
        raise NotImplementedError
