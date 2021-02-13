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
        response = app.response_class(
            response=jsonify(message="success"),
            status=200,
            mimetype='application/json'
        )
    except:
        response = app.response_class(
            response=jsonify(message="error"),
            status=500,
            mimetype='application/json'
        )
    return response


if __name__ == "__main__":
    app.run(debug=True)
