from Jasmin import Jasmin


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
        self.telnet.write(b'persist\n')

    def add_default_mt_router(self, smpp_client_id: str, rate: str = '0.0'):
        self.telnet.write(b'mtrouter -a\n')
        action = 'type ' + 'DefaultRoute' + '\n'
        self.telnet.write(action.encode('ascii'))
        action = 'connector smppc(' + smpp_client_id + ')\n'
        self.telnet.write(action.encode('ascii'))
        action = 'rate ' + rate + '\n'
        self.telnet.write(action.encode('ascii'))

        self.telnet.write(b'ok\n')
        self.telnet.write(b'persist\n')

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
        self.telnet.write(b'persist\n')

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
        self.telnet.write(b'persist\n')

    def remove_mo_router(self, order: int = 10):
        action = 'morouter -r ' + str(order)
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')

    def remove_mt_router(self, order: int = 10):
        action = 'mtrouter -r ' + str(order)
        self.telnet.write(action.encode('ascii') + b'\n')
        self.telnet.write(b'persist\n')
