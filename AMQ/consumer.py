import random
import string
from abc import ABC
from threading import Thread
import pika


class Consumer(ABC, Thread):
    def __init__(self, username='ADMIN', password='NONE', host='127.0.0.1', port=5672, queue=None):
        Thread.__init__(self)
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=self.credentials, heartbeat=0))
        self.__channel = self.connection.channel()
        self.__queue = queue if queue is not None else ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
        self.__channel.queue_declare(queue=self.__queue)
        self.__channel.basic_qos(prefetch_count=1)

    def get_channel(self):
        """
        :return pika.adapters.blocking_connection.BlockingChannel:
        """
        return self.__channel

    def close(self):
        self.connection.close()
