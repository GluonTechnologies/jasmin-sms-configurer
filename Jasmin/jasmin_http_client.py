from Jasmin import Jasmin


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
        self.telnet.write(b'persist\n')

    def remove_http_client(self, client_id: str = 'http_client_1'):
        action = 'httpccm -r ' + client_id
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')
