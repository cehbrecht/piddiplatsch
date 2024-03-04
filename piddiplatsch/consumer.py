import pika

from piddiplatsch.processor import get_message_processor


def do_consume(queue, type=None):
    c = PIDConsumer(queue, type)
    c.open_connection()
    c.start_consuming()


class PIDConsumer:
    def __init__(self, queue, type=None):
        self.queue = queue
        self.type = type
        self.channel = None

    def open_connection(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange="topic_birds", exchange_type="topic")

        self.channel.queue_declare(self.queue, exclusive=True)

        binding_key = "bird.*"
        self.channel.queue_bind(
            exchange="topic_birds", queue=self.queue, routing_key=binding_key
        )

    def start_consuming(self):
        print(" [*] Waiting for birds. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.on_message, auto_ack=True
        )
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, body):
        # print(f" [x] {method.routing_key}:{body}")
        p = get_message_processor(self.type)
        p.process_message(body)
