from Jasmin import Jasmin
import time


class JasminHttpClient(object):
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

    def add_http(self, url: str, client_id: str = 'http_client_1', method: str = 'POST'):
        self.telnet.write(b'httpccm -a\n')
        action = 'cid ' + client_id + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'url ' + url + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'method ' + method + '\n'
        self.telnet.write(action.encode('ascii'))
        self.telnet.write(b'ok\n')
        time.sleep(0.5)
        print("HTTP", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
        time.sleep(1)
        print("HTTP", self.telnet.read_very_eager())

    def remove_http_client(self, client_id: str = 'http_client_1'):
        action = 'httpccm -r ' + client_id
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')
        time.sleep(1)

    def process_http_action(self, json_action):
        if str(json_action['method']).lower() == 'add':
            if not json_action['data'].get('client_id') is None:
                self.add_http(url=json_action['data'].get('url'),
                              client_id=json_action['data'].get('client_id'),
                              method=json_action['data'].get('method'))
        elif str(json_action['method']).lower() == 'remove':
            if not json_action['data'].get('client_id') is None:
                self.remove_http_client(json_action['data'].get('client_id'))
