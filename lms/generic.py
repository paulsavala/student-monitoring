

class GenericApi:
    def __init__(self, api_token=None, api_url=None):
        self.api_token = api_token
        self.api_url = api_url
        self.lms = self._connect_to_lms()

    def _connect_to_lms(self):
        raise NotImplementedError

    def get_courses(self, instructor=None):
        # Return the Course object associated to this instructor
        raise NotImplementedError

    def get_course_grades(self, course=None):
        # Return the Grades object for this course
        raise NotImplementedError

    def get_student_grades(self, student=None):
        # Return the Grades object for this student
        raise NotImplementedError
