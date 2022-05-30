import sys

from flask import Flask, request
import uuid
import requests
import random
import socket
import hazelcast
import consul

def main():
    app = Flask(__name__)
    c = consul.Consul()
    print('here')
    c.agent.service.register('facade-service', service_id=sys.argv[1], port=int(sys.argv[1]))

    services = c.agent.services()

    messages_services = [f'http://127.0.0.1:{x[0]}/messages' for x in services.items() if x[1]['Service'] == 'message-service']
    logging_services = [f'http://127.0.0.1:{x[0]}/logging' for x in services.items() if x[1]['Service'] == 'logging-service']


    print('here')
    hz_client = hazelcast.HazelcastClient(cluster_name=c.kv.get('hz_cluster')[1]['Value'].decode('utf-8'),
                                          cluster_members=['127.0.0.1:'+c.kv.get('hz_node_1')[1]['Value'].decode('utf-8'),
                                                           '127.0.0.1:'+c.kv.get('hz_node_2')[1]['Value'].decode('utf-8'),
                                                           '127.0.0.1:'+c.kv.get('hz_node_3')[1]['Value'].decode('utf-8')])
    print('1')
    message_queue = hz_client.get_queue(c.kv.get('queue')[1]['Value'].decode('utf-8')).blocking()
    print('2')

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
        rq = request.get_json()
        id_ = uuid.uuid4()
        log = {'id': id_, 'text': rq.get("log")}
        msg = {'id': id_, 'text': rq.get("msg")}
        logging_service = random.choice(logging_services)

        if is_open(int(logging_service[17:21])):
            print('here')
            r = requests.post(logging_service, log)
            message_queue.put(msg)
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
            messages_resp = requests.get(random.choice(messages_services)).text
            print(str(logging_resp) + ":" + str(messages_resp))
            return str(logging_resp) + ":" + str(messages_resp)
        else:
            logging_services.remove(logging_service)
            return f'this logging service {logging_service[17:21]} was disconnected'

    app.run(host='127.0.0.1', port=int(sys.argv[1]), debug=True)


if __name__ == '__main__':
    print('facade service...')
    main()
