import sys

from flask import Flask, request
import hazelcast

app = Flask(__name__)
hz_client = hazelcast.HazelcastClient(cluster_name="HW3",
                                      cluster_members=[str(sys.argv[2])])
message_queue = hz_client.get_queue('msg_queue').blocking()
local_messages = []


@app.route('/messages', methods=['GET'])
def get_flow():
    while not message_queue.is_empty():
        local_messages.append(message_queue.take())
        print(f'read message: {local_messages[-1]}')
    return str(local_messages)


if __name__ == '__main__':
    print('messages service...')
    app.run(host='127.0.0.1', debug=True, port=int(sys.argv[1]))
