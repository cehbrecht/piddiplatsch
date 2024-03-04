#!/usr/bin/env python
import pika


def send_topic(message=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_birds", exchange_type="topic")

    routing_key = "bird.penguin"
    message = message or "Hello World!"
    channel.basic_publish(exchange="topic_birds", routing_key=routing_key, body=message)
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()
