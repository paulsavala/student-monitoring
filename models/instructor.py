

class Instructor:
    def __init__(self, name, department, api_token):
        self.name = name
        self.department = department
        self.api_token = api_token

    def get_courses(self):
        raise NotImplementedError
