from Jasmin import Jasmin
import time


class MORouter:
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

    def get_mo_routers(self):
        self.telnet.write(b'morouter -l\n')
        time.sleep(1)
        return self.telnet.read_very_eager()

    def add_default_mo_router(self, http_client_id: str):
        self.telnet.write(b'morouter -a\n')
        action = 'type ' + 'DefaultRoute' + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'connector http(' + http_client_id + ')\n'
        self.telnet.write(action.encode('ascii'))
        self.telnet.write(b'ok\n')
        time.sleep(0.5)
        print("MO-ROUTER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
        time.sleep(1)
        print("MO-ROUTER", self.telnet.read_very_eager())

    def add_mo_router(self, http_client_id: str, filters: str, order: int = 10, route_type: str = 'StaticMORoute'):
        self.telnet.write(b'morouter -a\n')
        action = 'type ' + route_type + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'order ' + str(order) + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'filters ' + str(filters) + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'connector http(' + http_client_id + ')\n'
        self.telnet.write(action.encode('ascii'))
        self.telnet.write(b'ok\n')
        time.sleep(1)
        print("MO-ROUTER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
        time.sleep(1)
        print("MO-ROUTER", self.telnet.read_very_eager())

    def remove_mo_router(self, order: int = 10):
        action = 'morouter -r ' + str(order)
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(1)
        print("MO-ROUTER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
