import telnetlib


class Jasmin(object):
    def __init__(self, username: str, password: str, host: str = '127.0.0.1', port: int = 8990):
        self.__user_name = username
        self.__password = password
        self.telnet: telnetlib.Telnet = telnetlib.Telnet(host, port=port)
        self.telnet.open(host, port=port)
        self.telnet.read_until(b'Authentication required.')
        self.telnet.write(self.__user_name.encode('ascii') + b"\n")
        self.telnet.write(self.__password.encode('ascii') + b"\n")
        # self.telnet.read_until(b'jcli :')
