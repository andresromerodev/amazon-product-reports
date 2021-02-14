from services import email_service


def run_asin_report():
    email_service.send_report('asin')
