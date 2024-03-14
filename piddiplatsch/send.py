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
        "file_size": 18028171468,
        "file_version": 1,
        "checksum": "312cb59854334b340d4d046310d028d08e0e71cfaa31ac031b383e1008594d42",
        "checksum_method": "SHA256",
        "is_part_of": "hdl:21.14100/37528ff1-2653-3c50-b670-7c00ba96fd6e",
        "url_original_data": f"http://vesg.ipsl.upmc.fr/thredds/fileServer/cmip6/{name}.nc",
        "url_replica": f"http://esgf3.dkrz.de/thredds/fileServer/cmip6/{name}.nc",
    }
    return message
