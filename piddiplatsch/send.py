#!/usr/bin/env python
import pika
import json


def send_topic(host, exchange, routing_key, title=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type="topic")

    message = build_message(title)
    data = json.dumps(message)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=data)
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()


def build_message(title):
    message = {
        "handle": "21.14106/TESTTESTTEST",
        "url_landing_page": "https://www.dkrz.de",
        "is_part_of": "hdl:21.14106/bla",
        "publisher": "WDCC at DKRZ",
        "aggregation_level": "dataset",
        "title": title,
        "entry_id": "blabliblu",
    }
    return message
