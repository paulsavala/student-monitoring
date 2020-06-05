from utils.models import add_to_list, remove_from_list


class Enrollment:
    def __init__(self, student, course, grades=None, current_score=None, ci_left=None, ci_right=None):
        self.student = student
        self.course = course
        self.grades = grades
        self.current_score = current_score
        self.ci_left = ci_left
        self.ci_right = ci_right

    def add_grades(self, grades):
        self.grades = add_to_list(self.grades, grades)

    def remove_grades(self, grades):
        self.grades = remove_from_list(self.grades, grades)
