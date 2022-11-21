from Jasmin import Jasmin


class JasminUser(object):
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

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
        self.telnet.write(b'persist\n')

    def remove_user(self, user_id: str):
        action = 'user -r ' + user_id
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')
