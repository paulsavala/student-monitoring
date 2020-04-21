from models.generic import GenericModel


class Assignment(GenericModel):
    def __init__(self, course, name, due_date, score):
        super().__init__()
        self.course = course
        self.name = name
        self.due_date = due_date
        self.score = score
