from Jasmin import Jasmin
import time


class MTRouter:
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

    def get_mt_routers(self):
        self.telnet.write(b'mtrouter -l\n')
        time.sleep(1)
        return self.telnet.read_very_eager()

    def add_default_mt_router(self, smpp_client_id: str, rate: str = '0.0'):
        self.telnet.write(b'mtrouter -a\n')
        action = 'type ' + 'DefaultRoute' + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'connector smppc(' + smpp_client_id + ')\n'
        self.telnet.write(action.encode('ascii'))
        action = 'rate ' + rate + '\n'
        self.telnet.write(action.encode('ascii'))
        self.telnet.write(b'ok\n')
        time.sleep(0.5)
        print("MT-ROUTER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
        time.sleep(1)
        print("MT-ROUTER", self.telnet.read_very_eager())

    def add_mt_router(self, smpp_client_id: str, filters: str = None, rate: str = '0.01', order: int = 10,
                      route_type: str = 'StaticMTRoute'):
        self.telnet.write(b'mtrouter -a\n')
        action = 'type ' + route_type + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'order ' + str(order) + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'filters ' + str(filters) + ';\n'
        self.telnet.write(action.encode('ascii'))
        action = 'connector smppc(' + smpp_client_id + ')\n'
        self.telnet.write(action.encode('ascii'))
        action = 'rate ' + rate + '\n'
        self.telnet.write(action.encode('ascii'))
        self.telnet.write(b'ok\n')
        time.sleep(0.5)
        print("MT-ROUTER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
        time.sleep(1)
        print("MT-ROUTER", self.telnet.read_very_eager())

    def remove_mt_router(self, order: int = 10):
        action = 'mtrouter -r ' + str(order)
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(1)
        print("MT-ROUTER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')
