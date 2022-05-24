from flask import Flask, request
import uuid
import requests

app = Flask(__name__)

logging_service = "http://localhost:8081/logging"
messages_service = "http://localhost:8082/messages"


@app.route('/facade', methods=['POST'])
def post_flow():
    message = {'id': uuid.uuid4(), 'text': request.get_json()}
    r = requests.post(logging_service, message)
    print(r.text)
    print(r.status_code)
    return r.text


@app.route('/facade', methods=['GET'])
def get_flow():
    logging_resp = requests.get(logging_service).text
    messages_resp = requests.get(messages_service).text
    print(str(logging_resp) + ":" + str(messages_resp))
    return str(logging_resp) + ":" + str(messages_resp)


if __name__ == '__main__':
    print('facade service...')
    app.run(host='localhost', port=8080, debug=True)
