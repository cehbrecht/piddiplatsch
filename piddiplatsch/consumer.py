import pika


def consume_topic(queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_birds", exchange_type="topic")

    channel.queue_declare(queue, exclusive=True)

    binding_key = "bird.*"
    channel.queue_bind(exchange="topic_birds", queue=queue, routing_key=binding_key)

    print(" [*] Waiting for birds. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        print(f" [x] {method.routing_key}:{body}")

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
