import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content

import os


sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


def send_sg_email(from_email, to_email, subject, content):
    from_email = Email(from_email)
    to_email = Email(to_email)
    content = Content(mime_type='text/html', content=content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code, response.body, response.headers
