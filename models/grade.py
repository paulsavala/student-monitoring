

class Grade:
    def __init__(self, student, course, assignment, score=None):
        self.student = student
        self.course = course
        self.assignment = assignment
        self.score = score

    def is_outlier(self, left, right):
        is_outlier = (self.score < left) or (self.score > right)
        return is_outlier
