import telnetlib
import socket


class Jasmin(object):
    def __init__(self, username: str = 'jcliadmin', password: str = 'jclipwd', host: str = '127.0.0.1',
                 port: int = 8990):
        self.__user_name = username
        self.__password = password
        host = socket.gethostbyname(host) if str(host).startswith('jasmin_sms_jasmin') else host
        self.telnet: telnetlib.Telnet = telnetlib.Telnet(host=host, port=port)
        self.telnet.open(host, port=port)
        self.telnet.read_until(b'Authentication required.')
        self.telnet.write(self.__user_name.encode('ascii') + b"\n")
        self.telnet.write(self.__password.encode('ascii') + b"\n")
        self.telnet.read_until(b'jcli :')
        print("Ready Now")
