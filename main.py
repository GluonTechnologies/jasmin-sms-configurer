import functools
import os
import threading
from AMQ import Consumer
from dotenv import load_dotenv
from Jasmin import Jasmin
from JasminAdmin import JasminProcess

load_dotenv()
host = os.getenv('AMPQ_HOST', '127.0.0.1')
virtual_host = os.getenv('AMPQ_VHOST', '/')
port = os.getenv('AMPQ_PORT', '5672')
username = os.getenv('AMPQ_USERNAME', 'admin')
password = os.getenv('AMPQ_PASSWORD', 'password123')
queueName = os.getenv('AMPQ_QUEUE_NAME', 'gluon.jasmin_sms')
exchangeName = os.getenv('AMPQ_EXCHANGE_NAME', 'gluon.smpp.exchange')

jasmin_telnet_host = os.getenv('JASMIN_TELNET_HOST', '127.0.0.1')
jasmin_telnet_port = os.getenv('JASMIN_TELNET_PORT', 8990)
jasmin_cli_username = os.getenv('JASMIN_CLI_USERNAME', 'jcliadmin')
jasmin_cli_password = os.getenv('JASMIN_CLI_PASSWORD', 'jclipwd')

consumer = Consumer(username=username, password=password, host=host, port=port, queue=queueName,
                    virtual_host=virtual_host)
channel = consumer.get_channel()
jasmin = Jasmin(username=jasmin_cli_username, password=jasmin_cli_password, host=jasmin_telnet_host,
                port=jasmin_telnet_port)
jasmin_processor = JasminProcess(jasmin=jasmin)


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
    print("Task Received:")
    print("\n")
    print(body)
    print("\n\n")
    if jasmin_processor.process(body):
        pass
    else:
        print("Whoops! error occurred.")
    cb = functools.partial(ack_message, chn, delivery_tag)
    connection.add_callback_threadsafe(cb)


def on_message(chn, method_frame, header_frame, body, args):
    (connection, _threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, chn, delivery_tag, body))
    t.daemon = True
    t.start()


on_message_callback = functools.partial(on_message, args=(channel.connection, []))
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queueName, on_message_callback=on_message_callback)
try:
    print("Consuming configuration tasks . . .")
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
channel.close()
