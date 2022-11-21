import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error


class JasminAPI(object):
    def __init__(self, username: str, password: str, jasmin_host='http://jasmin_sms_jasmin:1401'):
        self.root_url = jasmin_host
        self.username = username
        self.password = password

    def send_sms(self, params: dict):
        message_body = {'username': self.username, 'password': self.password, **params}
        urllib.request.urlopen(self.root_url + "/send?%s" % urllib.parse.urlencode(message_body)).read()
