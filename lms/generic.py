

class GenericApi:
    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key
        self.api_url = api_url

    def get_courses(self, instructor=None, course=None):
        raise NotImplementedError

    def get_grades(self, course=None, student=None):
        raise NotImplementedError

    def get_assignments(self, course=None, student=None):
        raise NotImplementedError