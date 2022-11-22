import socket
import requests


class JasminAPI(object):
    def __init__(self, username: str = 'gluon', password: str = 'password', jasmin_host='jasmin_sms_jasmin',
                 delivery_url='http://127.0.0.1/received'):
        jasmin_host = socket.gethostbyname(jasmin_host) if str(jasmin_host).startswith(
            'jasmin_sms_jasmin') else jasmin_host
        jasmin_host = 'http://' + jasmin_host + ':1401/send?%s'
        self.root_url = jasmin_host
        self.delivery_url = delivery_url
        self.username = username
        self.password = password

    def send_sms(self, params: dict):
        message_body = {'username': self.username, 'password': self.password, **params}
        # resp = urllib.request.urlopen(self.root_url + "/send?%s" % urllib.parse.urlencode(message_body)).read()
        resp = requests.get(self.root_url, params=message_body)

    def send_sms_data(self, params: dict):
        print('send_sms_data')
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
        print(self.root_url)
        resp = requests.get(self.root_url, params=message_body)
        print(resp.content)
