import json


class MessageProcessor:
    def process_message(self, message):
        data = json.loads(message)
        print(f"We got a message: {data}")
        record = self.create_handle_record(data)
        if not self.validate_handle_record(record):
            raise ValueError(f"handle record is not vaild: {record}")

    def create_handle_record(self, data):
        raise NotImplementedError

    def validate_handle_record(self, record):
        return False
