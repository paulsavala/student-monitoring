from models.generic import GenericModel


class Grades(GenericModel):
    def __init__(self, course, name, due_date, score):
        super().__init__()
        self.course = course
        self.name = name
        self.due_date = due_date
        self.score = score

    def form_ci(self, level=0.01):
        raise NotImplementedError

    def identify_outliers(self):
        raise NotImplementedError
