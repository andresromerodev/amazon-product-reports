import logging

from flask import Flask, jsonify
from services import email_service
from flask_apscheduler import APScheduler
from reports.reports import run_asin_report


app = Flask(__name__)
app.logger.setLevel(logging.INFO)

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


@scheduler.task('cron', id='job_run_reports', week='*',
                day_of_week='mon,tue,wed,thu,fri,sat', hour='15', minute='10')
def job_run_reports():
    app.logger.info('Running job_run_reports()')
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
    app.run(host='0.0.0.0', port=5000, debug=True)
