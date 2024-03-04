from piddiplatsch.processor.base import MessageProcessor


class DefaultProcessor(MessageProcessor):
    def do_process_message(self, data):
        msg = data.get("message")
        print(f"We got a message: {msg}")
