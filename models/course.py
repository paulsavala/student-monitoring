from utils.models import add_to_list, remove_from_list


class Course:
    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name

        self.students = None
        self.assignments = None

    def add_students(self, students):
        self.students = add_to_list(self.students, students)

    def remove_students(self, students):
        self.students = remove_from_list(self.students, students)

    def add_assignments(self, assignments):
        self.assignments = add_to_list(self.assignments, assignments)

    def remove_assignments(self, assignments):
        self.assignments = remove_from_list(self.assignments, assignments)

    def context_dict(self, course_outliers, course_summary):
        # Jinja context dictionary
        context_dict = dict(
            course=self,
            course_outliers=course_outliers,
            course_summary=course_summary
        )
        return context_dict
