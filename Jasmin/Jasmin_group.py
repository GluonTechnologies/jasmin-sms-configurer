from Jasmin import Jasmin
import time


class JasminGroup(object):
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

    def get_groups(self):
        self.telnet.write(b'group -l\n')
        time.sleep(1)
        return self.telnet.read_very_eager()

    def add_group(self, name: str):
        self.telnet.write(b'group -a\n')
        action = 'gid ' + name + '\n'
        self.telnet.write(action.encode('ascii'))
        self.telnet.write(b'ok\n')
        time.sleep(0.5)
        print("GROUP", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
        time.sleep(1)
        print("GROUP", self.telnet.read_very_eager())

    def remove_group(self, name: str):
        action = 'group -r ' + name
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(1)
        print("GROUP", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')

    def process_group_action(self, json_action):
        if str(json_action['method']).lower() == 'add':
            if not json_action['data'].get('name') is None:
                self.add_group(json_action['data'].get('name'))
        elif str(json_action['method']).lower() == 'remove':
            if json_action['data'].get('name') is not None:
                self.remove_group(json_action['data'].get('name'))
        elif str(json_action['method']).lower() == 'get':
            print("Return Results")
            return {'groups': str(self.get_groups())}
