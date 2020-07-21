from utils.models import add_to_list, remove_from_list
from utils.email import send_sg_email

from datetime import date
import datetime


class Instructor:
    def __init__(self, first_name, last_name, email, lms_id, courses=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.lms_id = lms_id
        self.courses = courses

    def add_courses(self, courses):
        self.courses = add_to_list(self.courses, courses)

    def remove_courses(self, courses):
        self.courses = remove_from_list(self.courses, courses)

    @staticmethod
    def render_email(context_dict, env):
        email_template = env.get_template('email/container.html')
        rendered_email = email_template.render(context_dict)
        return rendered_email

    def send_email(self, from_email, rendered_email):
        to_email = self.email
        week_start = (date.today() - datetime.timedelta(days=8)).strftime('%b %-d')
        week_end = (date.today() - datetime.timedelta(days=1)).strftime('%b %-d')
        subject = f'Student monitoring for {week_start} to {week_end}'
        response_code, response_body, response_headers = send_sg_email(from_email, to_email, subject, rendered_email)
        print(f'Email sent to {self.email}: Response = {response_code}')
        return response_code, response_body, response_headers
