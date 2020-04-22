from models. generic import GenericModel


class Instructor(GenericModel):
    def __init__(self, name, email, lms_id):
        super().__init__()
        self.name = name
        self.email = email
        self.lms_id = lms_id

        self.courses = None

    def get_courses(self):
        if self.courses is not None:
            return self.courses
        else:
            self.courses = self.lms.get_courses(self)
            return self.courses
