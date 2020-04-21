from models.generic import GenericModel


class Student(GenericModel):
    def __init__(self, name, student_id):
        super().__init__()
        self.name = name
        self.student_id = student_id

    def get_grades(self, course):
        raise NotImplementedError
