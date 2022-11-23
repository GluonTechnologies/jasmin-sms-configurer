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
ACTION = 'add'
# -----------------------------------------------------

# CONFIGURATION PARAMS
# -----------------------------------------------------
GROUP_NAME = 'group1'
HTTP_CLIENT_ID = 'http1'
SMPP_CLIENT_ID = 'smpp1'
SMPP_HOST = '10.190.10.16'
SMPP_PORT = '8331'
SMPP_USER = 'gluon'
SMPP_PASSWORD = 'password'
# -----------------------------------------------------
#######################################################

configs = [
    {'task': 'configure', 'action': 'group', 'method': ACTION, 'data': {'name': GROUP_NAME}},
    {'task': 'configure', 'action': 'user', 'method': ACTION,
     'data': {'username': 'gluon', 'password': 'password', 'group': GROUP_NAME}},
    {'task': 'configure', 'action': 'http', 'method': ACTION,
     'data': {'url': 'http://127.0.0.1:8000/received_message', 'method': 'POST', 'client_id': HTTP_CLIENT_ID}},
    {'task': 'configure', 'action': 'smpp', 'method': ACTION,
     'data': {'smpp_id': SMPP_CLIENT_ID, 'host': SMPP_HOST, 'port': SMPP_PORT, 'username': SMPP_USER,
              'password': SMPP_PASSWORD}},
    {'task': 'configure', 'action': 'mo-router', 'method': ACTION, 'data': {'http_client_id': HTTP_CLIENT_ID}},
    {'task': 'configure', 'action': 'mt-router', 'method': 'add', 'data': {'smpp_client_id': SMPP_CLIENT_ID}}
]

publisher = Publisher(username=username, password=password, host=host, port=port, virtual_host=virtual_host)

for config in configs:
    print("Configuring ", config['action'])
    publisher.publish(message=json.dumps(config), queue=queueName, exchange='exchange', routing_key='some_secure_key')
    time.sleep(2)
