from Jasmin import Jasmin
from Jasmin import JasminGroup
from Jasmin import JasminUser
from Jasmin import JasminSmppClient
from Jasmin import JasminHttpClient


class JasminAdmin(JasminGroup, JasminUser, JasminSmppClient, JasminHttpClient):
    def __init__(self, jasmin: Jasmin):
        super().__init__(jasmin)
