

class Course:
    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name

        self.students = None

    def create_summary(self):
        raise NotImplementedError

    def create_email(self):
        raise NotImplementedError
