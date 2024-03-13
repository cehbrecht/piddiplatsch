import json
from piddiplatsch.pidmaker import PidMaker

import logging

LOGGER = logging.getLogger("piddiplatsch")


class MessageProcessor:
    def __init__(self) -> None:
        self.pid_maker = PidMaker()
        self._binding_key = None
        self.configure()

    def configure(self):
        raise NotImplementedError

    @property
    def queue_name(self):
        return f"queue_{self.binding_key}"

    @property
    def binding_key(self):
        return self._binding_key

    def on_message(self, ch, method, properties, body):
        LOGGER.info(f"consume routing key: {method.routing_key}")
        try:
            self.process_message(body)
        except Exception:
            LOGGER.exception(f"message processing failed")
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def process_message(self, message):
        data = json.loads(message)
        LOGGER.info(f"We got a message: {data}")
        handle = self.create_handle(data)
        record = self.create_handle_record(data)
        if not self.validate_handle_record(record):
            raise ValueError(f"handle record is not vaild: {record}")
        self.pid_maker.create_handle(handle, record)

    def create_handle(self, data):
        handle = data.get("handle")
        handle = handle.lstrip("hdl:")
        return handle

    def create_handle_record(self, data):
        raise NotImplementedError

    def validate_handle_record(self, record):
        return False
