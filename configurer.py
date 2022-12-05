import time
from AMQ import Publisher
from dotenv import load_dotenv
import json

load_dotenv()
host = 'vulture.rmq.cloudamqp.com'
virtual_host = 'xabzsegw'
port = '5672'
username = 'xabzsegw'
password = 'RbEbEDiBbwENFz-BOB8uo-DOPlRFaMqQ'
queueName = 'gluon.smpp.001'

#######################################################
# GLUON SMS CONFIGURATION ACTIONS
# -----------------------------------------------------
ADD_ACTION = 'add'
# -----------------------------------------------------

# CONFIGURATION PARAMS
# -----------------------------------------------------
GROUP_NAME = 'group1'
HTTP_CLIENT_ID = 'http1'
SMPP_CLIENT_ID = 'smpp1'
SMPP_HOST = '192.168.174.126'
SMPP_PORT = '2778'
SMPP_USER = '014978'
SMPP_PASSWORD = 'Far$4321'
# -----------------------------------------------------
#######################################################

configs = [
    {'task': 'configure', 'action': 'group', 'method': ADD_ACTION, 'data': {'name': GROUP_NAME}},
    {'task': 'configure', 'action': 'user', 'method': ADD_ACTION,
     'data': {'username': 'gluon', 'password': 'password', 'group': GROUP_NAME}},
    {'task': 'configure', 'action': 'http', 'method': ADD_ACTION,
     'data': {'url': 'http://jasmin_sms_sync_api:5000/received_message', 'method': 'POST', 'client_id': HTTP_CLIENT_ID}},
    {'task': 'configure', 'action': 'smpp', 'method': ADD_ACTION,
     'data': {'smpp_id': SMPP_CLIENT_ID, 'host': SMPP_HOST, 'port': SMPP_PORT, 'username': SMPP_USER,
              'password': SMPP_PASSWORD}},
    {'task': 'configure', 'action': 'mo-router', 'method': ADD_ACTION, 'data': {'http_client_id': HTTP_CLIENT_ID}},
    {'task': 'configure', 'action': 'mt-router', 'method': ADD_ACTION, 'data': {'smpp_client_id': SMPP_CLIENT_ID}},
    {'task': 'configure', 'action': 'smpp', 'method': 'start',
     'data': {'smpp_id': SMPP_CLIENT_ID, 'host': SMPP_HOST, 'port': SMPP_PORT, 'username': SMPP_USER,
              'password': SMPP_PASSWORD}},
]

publisher = Publisher(username=username, password=password, host=host, port=port, virtual_host=virtual_host)

for config in configs:
    print("Configuring ", config['action'])
    publisher.publish(message=json.dumps(config), queue=queueName, exchange='exchange', routing_key='some_secure_key')
    time.sleep(2)

# publisher.publish(message=json.dumps(configs[2]), queue=queueName, exchange='exchange', routing_key='some_secure_key')
