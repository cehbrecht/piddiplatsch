#!/usr/bin/env python
import pika
import json


def send_topic(exchange, routing_key, message=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type="topic")

    message = message or "Hello World!"
    data = json.dumps({"message": message})
    channel.basic_publish(exchange="topic_birds", routing_key=routing_key, body=data)
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()
