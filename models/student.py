

class Student:
    def __init__(self, name, lms_id):
        self.name = name
        self.lms_id = lms_id

        self.assignment_collections = None
        self.assignment_map = None
        self.ci_left = None
        self.ci_right = None

    def set_assignments(self, assignment_collections):
        if not isinstance(assignment_collections, list):
            assignment_collections = [assignment_collections]
        self.assignment_collections = assignment_collections
        self.assignment_map = {ac.course: ac for ac in self.assignment_collections}

    def remove_assignments(self, course):
        assert self.assignment_collections is not None and course in self.assignment_collections, \
            'Student has no assignments for this course'
        del self.assignment_collections[course]

    def get_course_assignments(self, course):
        assert self.assignment_collections is not None, 'Student has no grades'
        return self.assignment_map.get(course)

    def set_ci(self, left, right):
        self.ci_left = left
        self.ci_right = right
