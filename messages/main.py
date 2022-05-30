import sys

from flask import Flask, request
import hazelcast
import consul

def main():
    app = Flask(__name__)

    c = consul.Consul()

    c.agent.service.register('message-service', service_id=sys.argv[1], port=int(sys.argv[1]))

    hz_client = hazelcast.HazelcastClient(cluster_name=c.kv.get('hz_cluster')[1]['Value'].decode('utf-8'),
                                          cluster_members=['127.0.0.1:'+c.kv.get('hz_node_1')[1]['Value'].decode('utf-8'),
                                                           '127.0.0.1:'+c.kv.get('hz_node_2')[1]['Value'].decode('utf-8'),
                                                           '127.0.0.1:'+c.kv.get('hz_node_3')[1]['Value'].decode('utf-8')])

    message_queue = hz_client.get_queue(c.kv.get('queue')[1]['Value'].decode('utf-8')).blocking()
    local_messages = []

    @app.route('/messages', methods=['GET'])
    def get_flow():
        while not message_queue.is_empty():
            local_messages.append(message_queue.take())
            print(f'read message: {local_messages[-1]}')
        return str(local_messages)

    app.run(host='127.0.0.1', debug=True, port=int(sys.argv[1]))


if __name__ == '__main__':
    print('messages service...')
    main()
