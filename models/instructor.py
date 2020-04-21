from models. generic import GenericModel
from models.course import Course


class Instructor(GenericModel):
    def __init__(self, name, email, api_token):
        super().__init__()
        self.name = name
        self.email = email
        self.api_token = api_token

        self.courses = None

    def get_courses(self):
        if self.courses is not None:
            return self.courses
        else:
            self.courses = self.lms.get_courses(self)
