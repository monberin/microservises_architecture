from flask import Flask, request
import uuid
import requests
import random
import socket
app = Flask(__name__)

messages_service = "http://127.0.0.1:9081/messages"

logging_services = ["http://127.0.0.1:9082/logging",
                    "http://127.0.0.1:9083/logging",
                    "http://127.0.0.1:9084/logging"]

def is_open(port):
    # https://www.adamsmith.haus/python/answers/how-to-check-if-a-network-port-is-open-in-python
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()
    if result_of_check == 0:
        return True
    return False


@app.route('/facade', methods=['POST'])
def post_flow():
    message = {'id': uuid.uuid4(), 'text': request.get_json()}
    logging_service = random.choice(logging_services)
    if is_open(int(logging_service[17:21])):
        r = requests.post(logging_service, message)
        print(r.text)
        print(r.status_code)
        return r.text

    else:
        logging_services.remove(logging_service)
        return f'this logging service {logging_service[17:21]} was disconnected'


@app.route('/facade', methods=['GET'])
def get_flow():
    logging_service = random.choice(logging_services)
    if is_open(int(logging_service[17:21])):
        logging_resp = requests.get(logging_service).text
        messages_resp = requests.get(messages_service).text
        print(str(logging_resp) + ":" + str(messages_resp))
        return str(logging_resp) + ":" + str(messages_resp)
    else:
        logging_services.remove(logging_service)
        return 'this logging service was disconnected'


if __name__ == '__main__':
    print('facade service...')
    app.run(host='localhost', port=9080, debug=True)
