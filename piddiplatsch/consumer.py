import pika

from piddiplatsch.processor import get_message_processor

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
        self.queue = exchange
        self.channel = None

    def open_connection(self, host):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")

        routing_key = f"{self.queue}.*"

        self.channel.queue_declare(self.queue, exclusive=True)

        self.channel.queue_bind(
            exchange=self.exchange, queue=self.queue, routing_key=routing_key
        )

    def start_consuming(self):
        LOGGER.info("Waiting for messages. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.on_message, auto_ack=True
        )
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, body):
        print(f" [x] {method.routing_key}")
        p = get_message_processor(method.routing_key)
        try:
            p.process_message(body)
        except ValueError as e:
            print(f"message processing failed: {e}")
