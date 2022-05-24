from flask import Flask, request

app = Flask(__name__)

messages = dict()


@app.route('/logging', methods=['POST'])
def post_flow():
    id = request.form['id']
    text = request.form['text']
    messages[id] = text
    print(text)
    print(list(messages.items()))
    return ''


@app.route('/logging', methods=['GET'])
def get_flow():
    return str(list(messages.items()))


if __name__ == '__main__':
    print('logging service...')
    app.run(host='localhost', port=8081, debug=True)
