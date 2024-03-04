from piddiplatsch.processor.base import MessageProcessor


class DefaultProcessor(MessageProcessor):
    def process_message(self, message):
        print(f"We got a message: {message}")
