from Jasmin import Jasmin
import time


class JasminRouter(object):
    def __init__(self, jasmin: Jasmin):
        self.telnet = jasmin.telnet

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

    def add_mt_router(self, smpp_client_id: str, filters: str, rate: str = '0.01', order: int = 10,
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

    def remove_mo_router(self, order: int = 10):
        action = 'morouter -r ' + str(order)
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(1)
        print("MO-ROUTER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')

    def remove_mt_router(self, order: int = 10):
        action = 'mtrouter -r ' + str(order)
        self.telnet.write(action.encode('ascii') + b'\n')
        time.sleep(1)
        print("MT-ROUTER", self.telnet.read_very_eager())
        self.telnet.write(b'persist\n')

    def process_mt_router_action(self, json_action):
        if str(json_action['method']).lower() == 'add':
            if not json_action['data'].get('smpp_client_id') is None:
                if not json_action['data'].get('filters') is None:
                    self.add_mt_router(smpp_client_id=json_action['data'].get('smpp_client_id'),
                                       filters=json_action['data'].get('filters'),
                                       rate=json_action['data'].get('rate'),
                                       order=json_action['data'].get('order'),
                                       route_type=json_action['data'].get('route_type'))
                else:
                    self.add_default_mt_router(smpp_client_id=json_action['data'].get('smpp_client_id'),
                                               rate=json_action['data'].get('rate'))
        elif str(json_action['method']).lower() == 'remove':
            if not json_action['data'].get('order') is None:
                self.remove_mt_router(json_action['data'].get('order'))

    def process_mo_router_action(self, json_action):
        if str(json_action['method']).lower() == 'add':
            if not json_action['data'].get('smpp_client_id') is None:
                if not json_action['data'].get('filters') is None:
                    self.add_mo_router(http_client_id=json_action['data'].get('smpp_client_id'),
                                       filters=json_action['data'].get('filters'),
                                       order=json_action['data'].get('order'),
                                       route_type=json_action['data'].get('route_type'))
                else:
                    self.add_default_mo_router(http_client_id=json_action['data'].get('smpp_client_id'))
        elif str(json_action['method']).lower() == 'remove':
            if not json_action['data'].get('order') is None:
                self.remove_mo_router(json_action['data'].get('order'))
