import requests
from flask import Flask
from flask import request, jsonify

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
        messages.append(message)
        copy = request.args.get('copy')
        if not copy:
            send_message_to_neighbour(message)

        response = jsonify({'status': 'received'})
        response.status_code = 201
        return response

    @app.route('/messages', methods=['GET'])
    def read_message():
        try:
            message = messages.pop()
            return message
        except IndexError:
            response = jsonify({"error": "no messages left"})
            response.status_code = 404
            return response

    def send_message_to_neighbour(message):
        try:
            payload = {'copy': True}
            r = requests.post(app.config['BACKUP_HOST'], data=message, params=payload, timeout=10)
        except Exception as e:
            app.logger.error("could not send to backup host reason: {0}".format(e))

    return app
