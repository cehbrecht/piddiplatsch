import pika

from piddiplatsch.handler import all_message_handlers

import logging


def logging_handler():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    ch.setFormatter(formatter)

    return ch


LOGGER = logging.getLogger("piddiplatsch")
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging_handler())


def do_consume(host, exchange):
    c = PIDConsumer(exchange)
    c.open_connection(host)
    c.start_consuming()


class PIDConsumer:
    def __init__(self, exchange):
        self.exchange = exchange
        self.channel = None

    def open_connection(self, host):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")

        for handler in all_message_handlers():
            self.create_queue(handler.queue_name, handler.binding_key)

    def create_queue(self, queue_name, binding_key):
        self.channel.queue_declare(queue_name, exclusive=True)
        self.channel.queue_bind(
            exchange=self.exchange, queue=queue_name, routing_key=binding_key
        )

    def start_consuming(self):
        LOGGER.info("Waiting for messages. To exit press CTRL+C")

        for handler in all_message_handlers():
            self.channel.basic_consume(
                queue=handler.queue_name,
                on_message_callback=handler.on_message,
                auto_ack=False,
            )
        self.channel.start_consuming()
