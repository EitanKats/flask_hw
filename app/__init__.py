import requests
from flask import Flask
from flask import request, jsonify, abort

from config import app_config

messages = []


def app_factory(config_name):
    if not config_name:
        config_name = 'development'
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    @app.route('/messages', methods=['POST'])
    def add_message():
        message = request.data
        copy = request.args.get('copy')
        if not copy:
            send_message_to_neighbour(message)

        messages.append(message)
        response = jsonify({'status': 'received'})
        response.status_code = 201
        return response

    @app.route('/messages', methods=['GET'])
    def read_message():
        try:
            copy = request.args.get('copy')
            if not copy:
                read_message_from_neighbour()
            message = messages.pop()

            return message
        except IndexError:
            abort(404, {"error": "no messages left"})

    def send_message_to_neighbour(message):
        if not app.config['SEND_BACKUP']:
            return

        try:
            payload = {'copy': True}
            requests.post(app.config['BACKUP_HOST'], data=message, params=payload, timeout=10)
        except Exception as e:
            abort(503, {'error': 'Backup server unavailable'})

    def read_message_from_neighbour():
        if not app.config['SEND_BACKUP']:
            return

        try:
            payload = {'copy': True}
            requests.get(app.config['BACKUP_HOST'], params=payload, timeout=10)
        except Exception as e:
            abort(503, {'error': 'Backup server unavailable'})

    return app
