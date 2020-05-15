

class Instructor:
    def __init__(self, name, email, lms_id, courses=None):
        self.name = name
        self.email = email
        self.lms_id = lms_id
        self.courses = courses

    def render_email(self, context_dict, env):
        email_template = env.get_template('email/container.html')
        rendered_email = email_template.render(context_dict)
        return rendered_email

    def send_email(self, rendered_email):
        raise NotImplementedError
