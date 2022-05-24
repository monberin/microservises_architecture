from flask import Flask, request

app = Flask(__name__)


@app.route('/messages', methods=['GET'])
def get_flow():
    return "not implemented yet"


if __name__ == '__main__':
    print('messages service...')
    app.run(host='localhost', port=8082, debug=True)
