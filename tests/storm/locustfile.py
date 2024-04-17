from locust import FastHttpUser, between, task

import json


# API endpoint for publishing messages to a queue
# https://www.freekb.net/Article?id=3108
PUBLISH_URL = "/api/exchanges/%2f/pids/publish"


class RabbitMQUser(FastHttpUser):
    host = "http://localhost:15672"
    wait_time = between(1, 5)

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

        data = json.dumps(message)

        # Message payload
        payload = {
            "properties": {},
            "routing_key": "cmip6.test",
            "payload": data,
            "payload_encoding": "string",
        }

        # Send the message to RabbitMQ
        with self.rest(
            "POST", PUBLISH_URL, json=payload, auth=("guest", "guest")
        ) as response:
            if response.js is None:
                pass  # no need to do anything, already marked as failed
            elif "routed" not in response.js:
                response.failure(f"'routed' missing from response {response.text}")
            elif response.js["routed"] is False:
                response.failure(
                    f"'routed' had an unexpected value: {response.js['routed']}"
                )
