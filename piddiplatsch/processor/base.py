import json


class MessageProcessor:
    def process_message(self, message):
        data = json.loads(message)
        print(f"We got a message: {data}")
        record = self.create_handle_record(data)
        print(record)

    def create_handle_record(self, data):
        raise NotImplementedError
