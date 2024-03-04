import json


class MessageProcessor:
    def process_message(self, message):
        data = json.loads(message)
        self.do_process_message(data)

    def do_process_message(self, data):
        raise NotImplementedError
