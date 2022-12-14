from Jasmin import Jasmin
from JasminAdmin import JasminAdmin
from AMQ import Publisher
from dotenv import load_dotenv
import json
import os


class JasminProcess(object):
    def __init__(self, jasmin: Jasmin):
        load_dotenv()
        host = os.getenv('AMPQ_HOST', '127.0.0.1')
        virtual_host = os.getenv('AMPQ_VHOST', '/')
        port = os.getenv('AMPQ_PORT', '5672')
        username = os.getenv('AMPQ_USERNAME', 'admin')
        password = os.getenv('AMPQ_PASSWORD', 'password123')

        self.queueName = os.getenv('AMPQ_QUEUE_NAME', 'gluon.smpp.queue')
        self.exchangeName = os.getenv('AMPQ_EXCHANGE_NAME', 'gluon.smpp.exchange')
        self.jasminAdmin = JasminAdmin(jasmin=jasmin)
        self.publisher = Publisher(username=username, password=password, host=host, port=port,
                                   virtual_host=virtual_host)
        self.id = {'action': 'CONFIGURE', 'method': 'ADD', }
        self.id = {'task': 'configure', 'action': 'group', 'method': 'add', 'data': {}}

    def process(self, message):
        try:
            json_message = json.loads(message)
            if not json_message.get('task') is None:
                if str(json_message['task']).lower() == 'configure':
                    self.process_configuration(json_message)

        except ValueError as e:
            return False
        return True

    def process_configuration(self, json_message):
        response = None
        if str(json_message['action']).lower() == 'group':
            response = self.jasminAdmin.group.process_group_action(json_message)
        elif str(json_message['action']).lower() == 'user':
            response = self.jasminAdmin.user.process_user_action(json_message)
        elif str(json_message['action']).lower() == 'smpp':
            response = self.jasminAdmin.smpp.process_smpp_action(json_message)
        elif str(json_message['action']).lower() == 'http':
            response = self.jasminAdmin.http.process_http_action(json_message)
        elif str(json_message['action']).lower() == 'mt-router':
            response = self.jasminAdmin.router.process_mt_router_action(json_message)
        elif str(json_message['action']).lower() == 'mo-router':
            response = self.jasminAdmin.router.process_mo_router_action(json_message)
        else:
            print("Whoops! Nothing to configure")
        if response is not None:
            self.publisher.publish(json.dumps(response), self.queueName + '.exceptions', self.exchangeName + '.error',
                                   self.exchangeName)
