from Jasmin import Jasmin
from Jasmin import JasminGroup
from Jasmin import JasminUser
from Jasmin import JasminSmppClient
from Jasmin import JasminHttpClient
from Jasmin import JasminRouter


class JasminAdmin(object):
    def __init__(self, jasmin: Jasmin):
        self.jasmin = jasmin
        self.group = JasminGroup(jasmin=jasmin)
        self.user = JasminUser(jasmin=jasmin)
        self.smpp = JasminSmppClient(jasmin=jasmin)
        self.http = JasminHttpClient(jasmin=jasmin)
        self.router = JasminRouter(jasmin=jasmin)
