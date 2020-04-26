from datetime import date


class Course:
    def __init__(self, course_id, name, instructor):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor

        self.students = None

    def create_email_card(self, course_outliers, course_summary, env):
        email_template = env.get_template('email/container.html')
        # Jinja context dictionary
        context_dict = dict(
            current_date=date.today().strftime('%m/%d/%Y'),
            instructor=self.instructor,
            course_outliers=course_outliers,
            course_summary=course_summary
        )
        rendered_email = email_template.render(context_dict)
        pass
