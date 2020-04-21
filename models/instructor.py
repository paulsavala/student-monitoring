from models. generic import GenericModel
from models.course import Course


class Instructor(GenericModel):
    def __init__(self, first_name, last_name, email, lms):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.lms = lms

        self.courses = None

    def get_courses(self):
        if self.courses is not None:
            return self.courses
        else:
            self.courses = self.lms.get_courses(self)
