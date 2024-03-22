import pika

from piddiplatsch.handler import filter_handlers

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


def do_consume(host, port, exchange, handlers, dry_run):
    c = PIDConsumer(exchange, handlers, dry_run)
    c.open_connection(host, port)
    c.start_consuming()


class PIDConsumer:
    def __init__(self, exchange, handlers, dry_run=False):
        self.exchange = exchange
        self.channel = None
        self.dry_run = dry_run
        self.enabled_handlers = filter_handlers(handlers)

    def create_queue(self, queue_name, binding_key):
        self.channel.queue_declare(queue_name, exclusive=True)
        self.channel.queue_bind(
            exchange=self.exchange, queue=queue_name, routing_key=binding_key
        )

    def open_connection(self, host, port):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port)
        )
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")

        for handler in self.enabled_handlers:
            self.create_queue(handler.queue_name, handler.binding_key)

    def start_consuming(self):
        LOGGER.info("Waiting for messages. To exit press CTRL+C")

        for handler in self.enabled_handlers:
            handler.dry_run = self.dry_run
            self.channel.basic_consume(
                queue=handler.queue_name,
                on_message_callback=handler.on_message,
                auto_ack=False,
            )
        self.channel.start_consuming()
