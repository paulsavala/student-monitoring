import sendgrid
from sendgrid.helpers.mail import Mail, Content

import os


sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


def send_sg_email(from_email, to_email, subject, content):
    content = Content(mime_type='text/html', content=content)
    mail = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code, response.body, response.headers
