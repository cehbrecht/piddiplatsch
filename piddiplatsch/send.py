#!/usr/bin/env python
import pika


def send_topic():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_birds", exchange_type="topic")

    routing_key = "bird.penguin"
    message = "Hello World!"
    channel.basic_publish(exchange="topic_birds", routing_key=routing_key, body=message)
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()


def send_hello():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
    print(" [x] Sent 'Hello World!'")
    connection.close()
