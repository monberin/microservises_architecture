import sys

from flask import Flask, request
import hazelcast
import consul

def main():
    app = Flask(__name__)

    c = consul.Consul()

    c.agent.service.register('logging-service', service_id=sys.argv[1], port=int(sys.argv[1]))

    hz_client = hazelcast.HazelcastClient(cluster_name=c.kv.get('hz_cluster')[1]['Value'].decode('utf-8'),
                                          cluster_members=['127.0.0.1:'+c.kv.get('hz_node_1')[1]['Value'].decode('utf-8'),
                                                           '127.0.0.1:'+c.kv.get('hz_node_2')[1]['Value'].decode('utf-8'),
                                                           '127.0.0.1:'+c.kv.get('hz_node_3')[1]['Value'].decode('utf-8')])
    print('2')
    # "127.0.0.1:5701",
    # "127.0.0.1:5702",
    # "127.0.0.1:5703",
    messages = hz_client.get_map(c.kv.get('map')[1]['Value'].decode('utf-8')).blocking()
    print('3')

    @app.route('/logging', methods=['POST'])
    def post_flow():
        id = request.form['id']
        text = request.form['text']
        messages.lock(id)
        try:
            messages.set(id, text)
        finally:
            messages.unlock(id)
        print(text)
        print(str(messages.values()))
        return ''

    @app.route('/logging', methods=['GET'])
    def get_flow():
        return str(messages.values())

    app.run(host='127.0.0.1', debug=True, port=int(sys.argv[1]))


if __name__ == '__main__':
    print('logging service...')
    main()
