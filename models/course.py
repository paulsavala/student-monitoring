

class Course:
    def __init__(self, department, number, instructor):
        self.department = department
        self.number = number
        self.instructor = instructor

    def get_students(self):
        raise NotImplementedError
