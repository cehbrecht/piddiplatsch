from locust import HttpUser, between, task, tag

import json
import pika
import time


class RabbitMQUser(HttpUser):
    host = "http://localhost:5672"
    wait_time = between(1, 5)

    # def on_start(self):
    #     # Establish connection to RabbitMQ server
    #     self.connection = pika.BlockingConnection(
    #         pika.ConnectionParameters(host="localhost", port=5672)
    #     )
    #     self.channel = self.connection.channel()

    #     self.channel.exchange_declare(exchange="pids", exchange_type="topic")

    # def on_stop(self):
    #     # Close RabbitMQ connection
    #     self.connection.close()

    @task
    def send_cmip6_message(self):
        # Define JSON message to be sent
        message = {
            "aggregation_level": "FILE",
            "file_name": "temp.nc",
            "file_size": 18028171468,
            "file_version": 1,
            "checksum": "312cb59854334b340d4d046310d028d08e0e71cfaa31ac031b383e1008594d42",
            "checksum_method": "SHA256",
            "is_part_of": "hdl:21.14100/37528ff1-2653-3c50-b670-7c00ba96fd6e",
            "url_original_data": "http://vesg.ipsl.upmc.fr/thredds/fileServer/cmip6/temp.nc",
            "url_replica": "http://esgf3.dkrz.de/thredds/fileServer/cmip6/temp.nc",
        }
        # Publish message to RabbitMQ queue
        # self.channel.basic_publish(
        #     exchange="pids", routing_key="cmip6.test", body=json.dumps(message)
        # )

        time.sleep(1)
        return True
