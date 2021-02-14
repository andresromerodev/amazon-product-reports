import json
from logging import error

from flask import Flask, jsonify
from dotenv import load_dotenv
from services import email_service

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

app = Flask(__name__)


@app.route('/api/v1/health', methods=['GET'])
def health():
    return jsonify(status='up')


@app.route('/api/v1/reports/run', methods=['POST'])
def run_report():
    return jsonify(message='Report is running')


@app.route('/api/v1/emails/send', methods=['POST'])
def send_email():
    response = None
    try:
        email_service.send_email()
        response = jsonify(message='success'), 200
    except Exception as e:
        response = jsonify(error=str(e)), 500
    return response


@app.route('/api/v1/reports/send', methods=['POST'])
def send_report():
    response = None
    try:
        email_service.send_report('asin')
        response = jsonify(message='success'), 200
    except Exception as e:
        response = jsonify(error=str(e)), 500
    return response


if __name__ == "__main__":
    app.run(debug=True)
