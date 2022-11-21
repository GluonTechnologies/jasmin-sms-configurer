from Jasmin import Jasmin


class JasminSmppClient(object):
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

    def add_smpp(self, username: str, password: str, host: str, port: int,
                 smpp_id: str = 'smpp_1', bind: str = 'transceiver'):
        self.telnet.write(b'smppccm -a\n')
        action = 'cid ' + smpp_id + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'username ' + username + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'password ' + password + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'host ' + host + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'port ' + str(port) + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'bind ' + bind + '\n'
        self.telnet.write(action.encode('ascii'))

        self.telnet.write(b'ok\n')
        self.telnet.write(b'persist\n')

    def stop_smpp_client(self, client_id: str = 'smpp_1'):
        action = 'smppccm -0 ' + client_id
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')

    def start_smpp_client(self, client_id: str = 'smpp_1'):
        action = 'smppccm -1 ' + client_id
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')

    def remove_smpp_client(self, client_id: str = 'smpp_1'):
        action = 'smppccm -r ' + client_id
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')
