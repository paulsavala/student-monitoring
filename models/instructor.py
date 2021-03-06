from utils.models import add_to_list, remove_from_list
from utils.email import send_sg_email

from datetime import date
import datetime
from logzero import logger


class Instructor:
    def __init__(self, first_name, last_name, email, lms_id, courses=None, color_blind_mode=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.lms_id = lms_id
        self.courses = courses
        self.color_blind_mode = color_blind_mode

    def add_courses(self, courses, allow_duplicates=False, unique_attr=None):
        self.courses = add_to_list(self.courses, courses, allow_duplicates, unique_attr)

    def remove_courses(self, courses, allow_duplicates=False, unique_attr=None):
        self.courses = remove_from_list(self.courses, courses, allow_duplicates, unique_attr)

    @staticmethod
    def render_email(context_dict, env):
        email_template = env.get_template('email/container.html')
        rendered_email = email_template.render(context_dict)
        return rendered_email

    def send_email(self, from_email, rendered_email):
        to_email = self.email
        week_start = (date.today() - datetime.timedelta(days=8)).strftime('%b %-d')
        week_end = (date.today() - datetime.timedelta(days=1)).strftime('%b %-d')
        subject = f'Grade report for {week_start} to {week_end}'
        response_code, response_body, response_headers = send_sg_email(from_email, to_email, subject, rendered_email)
        logger.info(f'Email sent to {self.email}: Response = {response_code}')
        return response_code, response_body, response_headers
