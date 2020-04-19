

class Student:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses

    def get_course(self, course_name, course_number):
        course = None
        for course in self.courses:
            if course.name == course_name and course.number == course_number:
                return course
        if course is None:
            raise AttributeError(f'Student is not enrolled in {course_name} {course_number}')
