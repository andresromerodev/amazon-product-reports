import sendgrid
import datetime
import os
from sendgrid.helpers.mail import *

API_KEY = api_key = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = api_key = os.environ.get('SENDGRID_FROM_EMAIL')
TO_EMAIL = api_key = os.environ.get('SENDGRID_TO_EMAIL')


def send_email():
    sg = sendgrid.SendGridAPIClient(API_KEY)
    from_email = Email(FROM_EMAIL)
    to_email = To(TO_EMAIL)

    today = datetime.datetime.now().strftime("%x")
    subject = "Daily ASIN Report " + today
    content = Content("text/plain", "Test Report")

    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)
