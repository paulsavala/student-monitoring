

class GenericApi:
    def __init__(self, api_url=None, api_token=None):
        self.api_url = api_url
        self.api_token = api_token
        self.lms = self._connect_to_lms()

    def _connect_to_lms(self):
        """
        Instantiate the API object and create the connection. Return the object.
        :return: Canvas object (API connection)
        """
        raise NotImplementedError

    def get_instructor(self):
        """
        Get Canvas user associated with this api key ('self' is a magic keyword to get the current user)
        :return: Instructor object
        """
        raise NotImplementedError

    def get_courses_by_instructor(self, instructor=None, semester=None):
        """
        Get all courses from Canvas for an instructor
        :param instructor: Instructor object
        :param semester: string showing the semester as it is stored in the LMS
        :return: List of dictionaries of the form {'id': course_lms_id, 'name': course_name}
        """
        raise NotImplementedError

    def get_students_in_course(self, course=None):
        """
        Get all students in a course
        :param course: Course object
        :return: List of dictionaries of the form {'name': student_name, 'lms_id': student_lms_id}
        """
        raise NotImplementedError

    def get_course_grades(self, course=None):
        """
        Get all grades for all students in the given course
        :param course: Course object
        :return: List of dictionaries of the form {student_lms_id: list of student assignments}. Student assignments
        are dictionaries of the form {'name': assignment_name, 'due_date': due_date, 'score': score}.
        """
        raise NotImplementedError

    def get_student_grades(self, student=None, course=None):
        """
        Get all grades for a single student in the given course. If you need all grades for all students in a course,
        use get_course_grades instead to reduce the number of API calls.
        :param student: Student object
        :param course: Course object
        :return: List of assignments. Assignments are dictionaries of the form
        {'name': assignment_name, 'due_date': due_date, 'score': score}
        """
        raise NotImplementedError
