import os
import socket
import requests


class JasminAPI(object):
    def __init__(self, username: str = 'gluon', password: str = 'password', jasmin_host='jasmin_sms_jasmin',
                 jasmin_port: int = 1401):
        jasmin_host = socket.gethostbyname(jasmin_host) if str(jasmin_host).startswith(
            'jasmin_sms_jasmin') else jasmin_host
        self.root_url = 'http://' + jasmin_host + ':' + str(jasmin_port) + '/send?%s'
        self.username = username
        self.password = password

        jasmin_sync_api_host = os.getenv('JASMIN_SMS_SYNC_API_HOST', '127.0.0.1')
        jasmin_sync_api_port = os.getenv('JASMIN_SMS_SYNC_API_PORT', '3001')
        delivery_host = socket.gethostbyname(jasmin_sync_api_host) if str(jasmin_sync_api_host).startswith(
            'jasmin_') else jasmin_sync_api_host
        self.delivery_url = 'http://' + delivery_host + ':' + str(jasmin_sync_api_port) + '/delivery_report'

    def send_sms(self, params: dict):
        message_body = {'username': self.username, 'password': self.password, **params}
        return requests.get(self.root_url, params=message_body)

    def send_sms_data(self, params: dict):
        message = params['message'] if params.get('message') else ''
        message_body = {
            'username': self.username,
            'password': self.password,
            'coding': '8',
            'dlr': 'yes',
            'dlr-url': self.delivery_url,
            'dlr-level': '3',
            'dlr-method': 'POST',
            'hex-content': message.encode('UTF-16BE').hex(),
            'to': params.get('to'),
            'from': params.get('from')
        }
        resp = requests.get(self.root_url, params=message_body)
        print(resp.content)
