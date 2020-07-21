import sendgrid
from sendgrid.helpers import mail as sg_mail

import os


sg_client = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


def send_sg_email(from_email, to_email, subject, content):
    from_email = sg_mail.Email(from_email)
    to_email = sg_mail.Email(to_email)
    content = sg_mail.Content(mime_type='text/html', content=content)
    mail = sg_mail.Mail(from_email, subject, to_email, content)
    response = sg_client.client.mail.send.post(request_body=mail.get())
    return response.status_code, response.body, response.headers
