from datetime import date


class Course:
    def __init__(self, course_id, name, instructor):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor

        self.students = None

    def context_dict(self, course_outliers, course_summary):
        # Jinja context dictionary
        context_dict = dict(
            course=self,
            course_outliers=course_outliers,
            course_summary=course_summary
        )
        return context_dict
