

class Instructor:
    def __init__(self, name, email, lms_id, courses=None):
        self.name = name
        self.email = email
        self.lms_id = lms_id
        self.courses = courses

    def send_email(self):
        raise NotImplementedError
