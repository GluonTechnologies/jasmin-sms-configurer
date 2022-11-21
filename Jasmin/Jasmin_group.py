from Jasmin import Jasmin


class JasminGroup(object):
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

    def get_groups(self):
        self.telnet.write(b'group -l\n')

    def add_group(self, name: str):
        self.telnet.write(b'group -a\n')
        action = 'gid ' + name
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'ok\n')
        self.telnet.write(b'persist\n')

    def remove_group(self, name: str):
        action = 'group -r ' + name
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')
