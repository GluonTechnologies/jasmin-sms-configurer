from Jasmin import Jasmin
import time


class JasminSmppClient(object):
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

    def get_smpp_clients(self):
        self.telnet.write(b'smppccm -l\n')
        time.sleep(1)
        return self.telnet.read_very_eager()

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
        time.sleep(0.5)
        print("SMPP", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
        time.sleep(1)
        print("SMPP", self.telnet.read_very_eager())

    def stop_smpp_client(self, client_id: str = 'smpp_1'):
        action = 'smppccm -0 ' + client_id
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(1)
        print("SMPP", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')

    def start_smpp_client(self, client_id: str = 'smpp_1'):
        action = 'smppccm -1 ' + client_id
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(1)
        print("SMPP", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')

    def remove_smpp_client(self, client_id: str = 'smpp_1'):
        action = 'smppccm -r ' + client_id
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(1)
        self.telnet.write(b'persist\n')

    def process_smpp_action(self, json_action):
        if str(json_action['method']).lower() == 'add':
            if not json_action['data'].get('smpp_id') is None:
                self.add_smpp(username=json_action['data'].get('username'),
                              password=json_action['data'].get('password'),
                              host=json_action['data'].get('host'),
                              port=json_action['data'].get('port'),
                              smpp_id=json_action['data'].get('smpp_id'))
        elif str(json_action['method']).lower() == 'start':
            if not json_action['data'].get('smpp_id') is None:
                self.start_smpp_client(json_action['data'].get('smpp_id'))
        elif str(json_action['method']).lower() == 'stop':
            if not json_action['data'].get('smpp_id') is None:
                self.stop_smpp_client(json_action['data'].get('smpp_id'))
        elif str(json_action['method']).lower() == 'remove':
            if not json_action['data'].get('smpp_id') is None:
                self.remove_smpp_client(json_action['data'].get('smpp_id'))
        elif str(json_action['method']).lower() == 'get':
            return {'smpp': str(self.get_smpp_clients())}
