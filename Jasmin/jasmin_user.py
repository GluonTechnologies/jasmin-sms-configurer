from Jasmin import Jasmin
import time


class JasminUser(object):
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

    def get_users(self):
        self.telnet.write(b'user -l\n')
        time.sleep(1)
        return self.telnet.read_very_eager()

    def add_user(self, username, password, group, user_id=None):
        self.telnet.write(b'user -a\n')
        action = 'username ' + username + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'password ' + password + '\n'
        self.telnet.write(action.encode('ascii'))
        user_id = str(username).lower() if user_id is None else str(user_id).lower()
        action = 'uid ' + user_id + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'gid ' + group + '\n'
        self.telnet.write(action.encode('ascii'))
        self.telnet.write(b'ok\n')
        time.sleep(0.5)
        print("USER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
        time.sleep(1)
        print("USER", self.telnet.read_very_eager())

    def remove_user(self, user_id: str):
        action = 'user -r ' + user_id
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(0.5)
        print("USER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')

    def process_user_action(self, json_action):
        if str(json_action['method']).lower() == 'add':
            if not json_action['data'].get('username') is None:
                self.add_user(username=json_action['data'].get('username'),
                              password=json_action['data'].get('password'),
                              group=json_action['data'].get('group'))
        elif str(json_action['method']).lower() == 'remove':
            if not json_action['data'].get('username') is None:
                self.remove_user(json_action['data'].get('username'))
        elif str(json_action['method']).lower() == 'get':
            return {'users': str(self.get_users())}
