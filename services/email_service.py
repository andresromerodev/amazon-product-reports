import sendgrid
import datetime
import base64
import os

from dotenv import load_dotenv
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition, Content, Email, To)

load_dotenv()

API_KEY = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL')
TO_EMAIL = os.environ.get('SENDGRID_TO_EMAIL')

sg = sendgrid.SendGridAPIClient(API_KEY)


def send_report(report_name):
    from_email = Email(FROM_EMAIL)
    to_email = To(TO_EMAIL)

    today = datetime.datetime.now().strftime('%x')
    subject = f'Daily ASIN Report {today}'
    content = Content(
        'text/plain', 'Please find attached the ASIN report for today')

    with open(f'./reports/{report_name}.xlsx', 'rb') as f:
        data = f.read()
        f.close()

    report = base64.b64encode(data).decode()

    file = Attachment(
        FileContent(report),
        FileName(f'ASIN_{today}.xlsx'),
        FileType('application/vnd.ms-excel'),
        Disposition('attachment')
    )

    mail = Mail(from_email, to_email, subject, content)
    mail.add_attachment(file)

    response = sg.send(mail)

    print(response.status_code)
    print(response.headers)
