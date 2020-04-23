

class GenericApi:
    def __init__(self, api_url=None, api_token=None):
        self.api_url = api_url
        self.api_token = api_token
        self.lms = self._connect_to_lms()

    def _connect_to_lms(self):
        # Create the connection to the LMS API
        raise NotImplementedError

    def get_courses(self, instructor=None):
        # Return the Course object associated to this instructor
        raise NotImplementedError

    def get_students_in_course(self, course=None):
        # Return a list of all Students in the course
        raise NotImplementedError

    def get_course_grades(self, course=None):
        # Return the Grades object for this course
        # Note: This should be faster than running self.get_student_grades() for students individually
        # due to running a single API call, rather than individual calls for each student.
        raise NotImplementedError

    def get_student_grades(self, student=None):
        # Return the Grades object for this student
        raise NotImplementedError
