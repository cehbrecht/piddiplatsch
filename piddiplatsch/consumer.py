import pika

from piddiplatsch.processor import get_message_processor


def do_consume(host, queue, exchange, routing_key, type=None):
    c = PIDConsumer(queue, type)
    c.open_connection(host, exchange, routing_key)
    c.start_consuming()


class PIDConsumer:
    def __init__(self, queue, type=None):
        self.queue = queue
        self.type = type
        self.channel = None

    def open_connection(self, host, exchange, routing_key):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange=exchange, exchange_type="topic")

        self.channel.queue_declare(self.queue, exclusive=True)

        self.channel.queue_bind(
            exchange=exchange, queue=self.queue, routing_key=routing_key
        )

    def start_consuming(self):
        print(" [*] Waiting for messages. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.on_message, auto_ack=True
        )
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, body):
        # print(f" [x] {method.routing_key}:{body}")
        p = get_message_processor(self.type)
        p.process_message(body)
