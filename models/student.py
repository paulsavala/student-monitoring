from models.generic import GenericModel


class Student(GenericModel):
    def __init__(self, name, lms_id):
        super().__init__()
        self.name = name
        self.lms_id = lms_id

        self.grades = None

    def set_grades(self, grades):
        raise NotImplementedError

    def create_summary(self):
        assert self.grades is not None, 'First run set_grades() to apply student grades'
        raise NotImplementedError
