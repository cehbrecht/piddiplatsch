import pika
import json


def send_topic(host, port, exchange, routing_key, file):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type="topic")

    data = json.dumps(json.load(open(file)))
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=data)
    print(f"Sent {routing_key}")
    connection.close()
