import sys

from flask import Flask, request
import hazelcast

def main():
    app = Flask(__name__)
    print(sys.argv[2])
    hz_client = hazelcast.HazelcastClient(cluster_name="HW3",
                                          cluster_members=[str(sys.argv[2])])

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

    app.run(host='127.0.0.1', debug=True, port=int(sys.argv[1]))
    
if __name__ == '__main__':
    print('logging service...')
    main()
