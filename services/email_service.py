import sendgrid
import datetime
import base64
import os

from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition, Content, Email, To)

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


def send_report(report_name):
    sg = sendgrid.SendGridAPIClient(API_KEY)
    from_email = Email(FROM_EMAIL)
    to_email = To(TO_EMAIL)

    today = datetime.datetime.now().strftime("%x")
    subject = "Daily ASIN Report " + today
    content = Content(
        "text/plain", "Please find attached the ASIN report for today")

    with open("C:/Users/andre/dev/amazon-product-reports/reports/asin.xlsx", 'rb') as f:
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
    print(response.body)
    print(response.headers)
