import pika


def consume_topic():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_birds", exchange_type="topic")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    binding_key = "bird.*"
    channel.queue_bind(
        exchange="topic_birds", queue=queue_name, routing_key=binding_key
    )

    print(" [*] Waiting for birds. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        print(f" [x] {method.routing_key}:{body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
