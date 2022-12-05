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
#                   'data': {'url': 'http://127.0.0.1:8000/received_message', 'method': 'POST', 'client_id': 'gluon_01'}}

# SMPP
# message_action = {'task': 'configure', 'action': 'smpp', 'method': 'start',
#                   'data': {'smpp_id': 'smpp1', 'host': '10.190.10.16', 'port': '8313', 'username': '014978',
#                            'password': 'Far$4321'}}

# ROUTER
# message_action = {'task': 'configure', 'action': 'mt-router', 'method': 'add',
#                   'data': {'smpp_client_id': 'smpp_1'}}

# message_action = {'task': 'configure', 'action': 'mo-router', 'method': 'add',
#                   'data': {'http_client_id': 'gluon_01'}}


# SMS

message_action = {'task': 'sms', 'action': 'send',
                  'data': {'to': '251944272962', 'from': '9543', 'message': 'ይህ በአማርኛ የተሞከረ መልዕክት ነው'}}
publisher.publish(message=json.dumps(message_action), queue=queueName, exchange='exchange',
                  routing_key='some_secure_key')
