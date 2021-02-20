import os
import logging

from dotenv import load_dotenv
from flask import Flask, jsonify
from services import email_service
from flask_apscheduler import APScheduler
from reports.reports import run_asin_report

REPORTS_JOB_ID = os.environ.get('REPORTS_JOB_ID')
REPORTS_CRON_WEEK = os.environ.get('REPORTS_CRON_WEEK')
REPORTS_CRON_DAYS = os.environ.get('REPORTS_CRON_DAYS')
REPORTS_CRON_HOUR = os.environ.get('REPORTS_CRON_HOUR')
REPORTS_CRON_MINUTE = os.environ.get('REPORTS_CRON_MINUTE')
REPORTS_CRON_TIMEZONE = os.environ.get('REPORTS_CRON_TIMEZONE')

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


@scheduler.task('cron', id=REPORTS_JOB_ID, week=REPORTS_CRON_WEEK,
                day_of_week=REPORTS_CRON_DAYS, hour=REPORTS_CRON_HOUR,
                minute=REPORTS_CRON_MINUTE, timezone=REPORTS_CRON_TIMEZONE)
def job_run_reports():
    app.logger.info('Running reports...')
    run_asin_report()


@app.route('/api/v1/health', methods=['GET'])
def health():
    return jsonify(status='up')


@app.route('/api/v1/reports/send/<report_name>', methods=['POST'])
def send_report(report_name):
    app.logger.info(f'Sending report: {report_name}')
    response = None
    try:
        email_service.send_report(report_name)
        response = jsonify(message='success'), 200
    except Exception as e:
        response = jsonify(error=str(e)), 500
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
