from models.generic import GenericModel


class Assignment(GenericModel):
    def __init__(self, student, assigment_name, due_date, score):
        super().__init__()
        self.student = student
        self.assigment_name = assigment_name
        self.due_date = due_date
        self.score = score


class AssignmentCollection(GenericModel):
    def __init__(self, student, course, assignments):
        super().__init__()
        self.student = student
        self.course = course
        self.assignments = assignments

    def form_ci(self, level=0.05):
        raise NotImplementedError

    def identify_outliers(self):
        raise NotImplementedError
