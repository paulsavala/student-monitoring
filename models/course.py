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

    # def create_email_card(self, course, course_outliers, course_summary, env):
    #     email_template = env.get_template('email/course_card.html')
    #     # Jinja context dictionary
    #     context_dict = dict(
    #         current_date=date.today().strftime('%m/%d/%Y'),
    #         instructor=self.instructor,
    #         course=course,
    #         course_outliers=course_outliers,
    #         course_summary=course_summary
    #     )
    #     rendered_card = email_template.render(context_dict)
    #     return rendered_card
