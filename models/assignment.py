from datetime import datetime


class Assignment:
    def __init__(self, lms_id, assignment_name, due_date, course):
        self.lms_id = lms_id
        self.assignment_name = assignment_name
        self.due_date = due_date
        self.course = course

        if isinstance(due_date, str):
            # todo: How can I pull this from the config instead? Don't want to pass the config due to circular imports,
            # todo: and I want this to work for any config.
            self.due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%SZ')

    def is_outlier(self, left, right):
        is_outlier = (self.score < left) or (self.score > right)
        return is_outlier
