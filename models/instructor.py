from utils.models import add_to_list, remove_from_list


class Instructor:
    def __init__(self, first_name, last_name, email, lms_id, courses=None, profile_pic=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.lms_id = lms_id
        self.courses = courses
        self.profile_pic = profile_pic

    def render_email(self, context_dict, env):
        email_template = env.get_template('email/container.html')
        rendered_email = email_template.render(context_dict)
        return rendered_email

    def send_email(self, rendered_email):
        raise NotImplementedError

    def add_courses(self, courses):
        self.courses = add_to_list(self.courses, courses)

    def remove_courses(self, courses):
        self.courses = remove_from_list(self.courses, courses)
