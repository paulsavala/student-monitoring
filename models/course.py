from utils.models import add_to_list, remove_from_list


class Course:
    def __init__(self, lms_id, short_name, alias=None):
        self.lms_id = lms_id
        self.short_name = short_name
        self.alias = alias

        self.students = None
        self.assignments = None

    def add_students(self, students, allow_duplicates=False, unique_attr=None):
        self.students = add_to_list(self.students, students, allow_duplicates, unique_attr)

    def remove_students(self, students, allow_duplicates=False, unique_attr=None):
        self.students = remove_from_list(self.students, students, allow_duplicates, unique_attr)

    def add_assignments(self, assignments, allow_duplicates=False, unique_attr=None):
        self.assignments = add_to_list(self.assignments, assignments, allow_duplicates, unique_attr)

    def remove_assignments(self, assignments, allow_duplicates=False, unique_attr=None):
        self.assignments = remove_from_list(self.assignments, assignments, allow_duplicates, unique_attr)

    def context_dict(self, course_outliers, course_summary):
        # Jinja context dictionary
        context_dict = dict(
            course=self,
            course_outliers=course_outliers,
            course_summary=course_summary
        )
        return context_dict
