from kombu import Connection, Exchange, Queue, Consumer
from socket import timeout as timeout_err
from logging import getLogger


class MessageProducer():
    def __init__(self, dsn, queue_name="notification"):
        self.dsn = dsn
        self.queue_name = queue_name

    def send_message(self, message):
        with Connection(self.dsn) as connection:
            with connection.SimpleQueue(name=self.queue_name) as reservation_queue:
                producer = connection.Producer()
                producer.publish(message, exchange=reservation_queue.exchange,
                                 routing_key=reservation_queue.routing_key)
