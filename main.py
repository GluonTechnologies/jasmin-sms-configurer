import functools
import json
import os
import threading
import time
import AMQ
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('AMPQ_HOST', '127.0.0.1')
port = os.getenv('AMPQ_PORT', '5672')
username = os.getenv('AMPQ_USERNAME', 'admin')
password = os.getenv('AMPQ_PASSWORD', 'password123')
queueName = os.getenv('QUEUE_NAME', 'record.finger_print')

consumer = AMQ.Consumer(username=username, password=password, host=host, port=port, queue=queueName)
channel = consumer.get_channel()


def ack_message(chn, delivery_tag, status=1):
    if chn.is_open:
        if status is None:
            chn.basic_nack(delivery_tag, multiple=False, requeue=True)
        else:
            chn.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass


def do_work(connection, chn, delivery_tag, body):
    pass


def on_message(chn, method_frame, header_frame, body, args):
    (connection, _threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, chn, delivery_tag, body))
    t.daemon = True
    t.start()


on_message_callback = functools.partial(on_message, args=(channel.connection, []))
channel.basic_consume(queue=queueName, on_message_callback=on_message_callback, auto_ack=False)
channel.start_consuming()
