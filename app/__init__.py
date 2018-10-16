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
            message = messages.pop()
            return message
        except IndexError:
            abort(404, {"error": "no messages left"})

    def send_message_to_neighbour(message):
        try:
            payload = {'copy': True}
            r = requests.post(app.config['BACKUP_HOST'], data=message, params=payload, timeout=10)
        except Exception as e:
            app.logger.error("could not send to backup host reason: {0}".format(e))
            abort(503, {'error': 'Backup server unavailable'})

    return app
