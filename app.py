from flask import Flask
from flask import request, jsonify, abort
import requests

from config import app_config

app = Flask(__name__)

messages = []


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/messages', methods=['POST'])
def add_message():
    messages.append(request.data)
    copy = request.args.get('copy')
    if copy:
        pass
    # send to neighbour server
    response = jsonify({'status': 'received'})
    response.status_code = 201
    return response


@app.route('/messages/read', methods=['GET'])
def read_message():
    return messages.pop()


if __name__ == '__main__':
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.run()
