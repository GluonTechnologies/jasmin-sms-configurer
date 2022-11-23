from threading import Thread
import pika


class Publisher(Thread):
    def __init__(self, username='ADMIN', password='NONE', host='127.0.0.1', port=5672, virtual_host='/'):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)
        self.virtual_host = virtual_host
        self.connection = None
        self.channel = None

    def publish(self, message, queue=None, exchange=None, routing_key=None):
        if not self.connection:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials,
                                          virtual_host=self.virtual_host))
            self.channel = self.connection.channel()

        if self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials,
                                          virtual_host=self.virtual_host))
            self.channel = self.connection.channel()
        if self.channel.is_closed:
            self.channel = self.connection.channel()

        self.channel.queue_declare(queue=queue)
        self.channel.exchange_declare(exchange=exchange, exchange_type='direct')
        self.channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        self.channel.close()
        self.connection.close()

    def close(self):
        self.connection.close()
