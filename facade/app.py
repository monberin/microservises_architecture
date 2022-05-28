from flask import Flask, request
import uuid
import requests
import random

app = Flask(__name__)

messages_service = "http://localhost:9081/messages"

logging_services = ["http://localhost:9082/logging",
                    "http://localhost:9083/logging",
                    "http://localhost:9084/logging"]


@app.route('/facade', methods=['POST'])
def post_flow():
    message = {'id': uuid.uuid4(), 'text': request.get_json()}
    r = requests.post(random.choice(logging_services), message)
    print(r.text)
    print(r.status_code)
    return r.text


@app.route('/facade', methods=['GET'])
def get_flow():
    logging_resp = requests.get(random.choice(logging_services)).text
    messages_resp = requests.get(messages_service).text
    print(str(logging_resp) + ":" + str(messages_resp))
    return str(logging_resp) + ":" + str(messages_resp)


if __name__ == '__main__':
    print('facade service...')
    app.run(host='localhost', port=9080, debug=True)
