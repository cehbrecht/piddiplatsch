import json
from piddiplatsch.pidmaker import PidMaker

import logging

LOGGER = logging.getLogger("piddiplatsch")


class MessageProcessor:
    def __init__(self) -> None:
        self.pid_maker = PidMaker()

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
