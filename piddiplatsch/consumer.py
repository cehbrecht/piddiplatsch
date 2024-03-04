import pika

from piddiplatsch.processor import get_message_processor


def do_consume(queue, type=None):
    c = PIDConsumer(queue, type)
    c.open_connection()


class PIDConsumer:
    def __init__(self, queue, type=None):
        self.queue = queue
        self.type = type

    def open_connection(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        channel.exchange_declare(exchange="topic_birds", exchange_type="topic")

        channel.queue_declare(self.queue, exclusive=True)

        binding_key = "bird.*"
        channel.queue_bind(
            exchange="topic_birds", queue=self.queue, routing_key=binding_key
        )

        print(" [*] Waiting for birds. To exit press CTRL+C")

        channel.basic_consume(
            queue=self.queue, on_message_callback=self.on_message, auto_ack=True
        )
        channel.start_consuming()

    def on_message(self, ch, method, properties, body):
        # print(f" [x] {method.routing_key}:{body}")
        p = get_message_processor(self.type)
        p.process_message(body)
