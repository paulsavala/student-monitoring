from datetime import datetime


class Assignment:
    def __init__(self, lms_id, assignment_name, due_date, course, datetime_format):
        self.lms_id = lms_id
        self.assignment_name = assignment_name
        self.due_date = due_date
        self.course = course
        self.datetime_format = datetime_format

        if isinstance(due_date, str):
            self.due_date = datetime.strptime(due_date, self.datetime_format)
