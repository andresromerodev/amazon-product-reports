import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from services import email_service
from reports.reports import run_asin_report
from tasks.task_scheduler import TaskScheduler

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
scheduler = TaskScheduler()

ASIN_REPORT_TIME = api_key = os.environ.get('ASIN_REPORT_TIME')


@app.route('/api/v1/health', methods=['GET'])
def health():
    return jsonify(status='up')


@app.route('/api/v1/reports/send', methods=['POST'])
def send_report():
    response = None
    try:
        email_service.send_report('asin')
        response = jsonify(message='success'), 200
    except Exception as e:
        response = jsonify(error=str(e)), 500
    return response


@app.before_first_request
def tasks_schedule_setup():
    scheduler.daily(time=ASIN_REPORT_TIME, task=run_asin_report)


if __name__ == "__main__":
    backgroud_tasks = scheduler.run_tasks_in_background()
    app.run(debug=True)
    backgroud_tasks.set()
