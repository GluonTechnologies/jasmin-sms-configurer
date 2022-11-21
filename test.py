import os
from AMQ import Publisher
from dotenv import load_dotenv
import json

load_dotenv()
host = os.getenv('AMPQ_HOST', '127.0.0.1')
virtual_host = os.getenv('AMPQ_VHOST', '/')
port = os.getenv('AMPQ_PORT', '5672')
username = os.getenv('AMPQ_USERNAME', 'admin')
password = os.getenv('AMPQ_PASSWORD', 'password123')
queueName = os.getenv('AMPQ_QUEUE_NAME', 'gluon.jasmin_sms')

publisher = Publisher(username=username, password=password, host=host, port=port, virtual_host=virtual_host)
# Goup Action
# message_action = {'task': 'configure', 'action': 'group', 'method': 'add', 'data': {'name': 'group_1'}}

# Users Action
# message_action = {'task': 'configure', 'action': 'user', 'method': 'add',
#                   'data': {'username': 'gluon', 'password': 'password', 'group': 'group_1'}}

# HTTP Actions
# message_action = {'task': 'configure', 'action': 'http', 'method': 'add',
#                   'data': {'url': 'http://10.10.20.125/receive-sms/mo.php', 'method': 'POST', 'client_id': 'gluon_01'}}

# SMPP
# message_action = {'task': 'configure', 'action': 'smpp', 'method': 'start',
#                   'data': {'smpp_id': 'smpp_1', 'host': '10.190.10.16', 'port': '8331', 'username': 'gluon',
#                            'password': 'password'}}

# ROUTER
message_action = {'task': 'configure', 'action': 'mt-router', 'method': 'add',
                  'data': {'smpp_id': 'smpp_1', 'host': '10.190.10.16', 'port': '8331', 'username': 'gluon',
                           'password': 'password'}}
publisher.publish(message=json.dumps(message_action), queue=queueName, exchange='exchange',
                  routing_key='some_secure_key')
