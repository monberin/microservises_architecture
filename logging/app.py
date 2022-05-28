from flask import Flask, request
import hazelcast

app = Flask(__name__)

hz_client = hazelcast.HazelcastClient(cluster_name="hw2",
                                       cluster_members=[
                                           "127.0.0.1:5701",
                                           "127.0.0.1:5702",
                                           "127.0.0.1:5703",
                                       ])
messages = hz_client.get_map('logging_map').blocking()


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


if __name__ == '__main__':
    print('logging service...')
    app.run(host='localhost', debug=True)
