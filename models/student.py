from utils.models import add_to_list, remove_from_list


class Student:
    def __init__(self, name, lms_id, enrollments=None):
        self.name = name
        self.lms_id = lms_id
        self.enrollments = enrollments

    def add_enrollments(self, enrollments, allow_duplicates=False, unique_attr=None):
        self.enrollments = add_to_list(self.enrollments, enrollments, allow_duplicates, unique_attr)

    def remove_enrollments(self, enrollments, allow_duplicates=False, unique_attr=None):
        self.enrollments = remove_from_list(self.enrollments, enrollments, allow_duplicates, unique_attr)

    def get_enrollment_by_course(self, course):
        assert self.enrollments is not None, 'Student has no enrollments'

        enrollment = [e for e in self.enrollments if e.course.lms_id == course.lms_id]
        assert len(enrollment) != 0, f'Student does not have an enrollment for course {course}'
        assert len(enrollment) == 1, f'Student has multiple enrollments for course {course}'
        return enrollment[0]
