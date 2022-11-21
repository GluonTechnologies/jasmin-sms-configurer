from Jasmin import Jasmin
from JasminAdmin import JasminAdmin
from JasminAdmin import JasminAPI
import json


class JasminProcess(object):
    def __init__(self, jasmin: Jasmin):
        self.jasminAdmin = JasminAdmin(jasmin=jasmin)
        self.jasminAPI = JasminAPI(username='', password='')
        self.id = {'action': 'CONFIGURE', 'method': 'ADD', }
        self.id = {'task': 'configure', 'action': 'group', 'method': 'add', 'data': {}}

    def process(self, message):
        try:
            json_message = json.loads(message)
            if not json_message.get('task') is None:
                if str(json_message['task']).lower() == 'configure':
                    self.process_configuration(json_message)
                elif str(json_message['task']).lower() == 'sms':
                    self.process_sms(json_message)

        except ValueError as e:
            return False
        return True

    def process_configuration(self, json_message):
        if str(json_message['action']).lower() == 'group':
            self.jasminAdmin.group.process_group_action(json_message)
        elif str(json_message['action']).lower() == 'user':
            self.jasminAdmin.user.process_user_action(json_message)
        elif str(json_message['action']).lower() == 'smpp':
            self.jasminAdmin.smpp.process_smpp_action(json_message)
        elif str(json_message['action']).lower() == 'http':
            self.jasminAdmin.http.process_http_action(json_message)
        elif str(json_message['action']).lower() == 'mt-router':
            self.jasminAdmin.router.process_mt_router_action(json_message)
        elif str(json_message['action']).lower() == 'mo-router':
            self.jasminAdmin.router.process_mo_router_action(json_message)
        else:
            print("Whoops! Nothing to configure")

    def process_sms(self, json_message):
        pass
