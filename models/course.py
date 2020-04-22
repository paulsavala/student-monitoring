from models.generic import GenericModel


class Course(GenericModel):
    def __init__(self, course_id, name):
        super().__init__()
        self.course_id = course_id
        self.name = name

    def get_students(self):
        raise NotImplementedError

    def create_summary(self):
        raise NotImplementedError

    def create_email(self):
        raise NotImplementedError
