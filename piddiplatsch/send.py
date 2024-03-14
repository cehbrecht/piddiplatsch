#!/usr/bin/env python
import pika
import json


def send_topic(host, port, exchange, routing_key, title=None):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type="topic")

    message = build_message(routing_key, title)
    data = json.dumps(message)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=data)
    print(f"Sent {routing_key}:{message}")
    connection.close()


def build_message(routing_key, title):
    if routing_key.startswith("wdcc"):
        msg = build_wdcc_message(title)
    elif routing_key.startswith("cmip6"):
        msg = build_cmip6_message(title)
    else:
        msg = ""
    return msg


def build_wdcc_message(name):
    message = {
        # "handle": handle,
        "url_landing_page": f"https://www.wdc-climate.de/ui/entry?acronym={name}",
        "is_part_of": f"hdl:21.14106/test_{name}",
        "publisher": "WDCC at DKRZ",
        "aggregation_level": "dataset",
        "title": name,
        "entry_id": "2426195",
    }
    return message


def build_cmip6_message(name):
    message = {
        "aggregation_level": "FILE",
        "file_name": f"{name}.nc",
    }
    return message
