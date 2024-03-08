from piddiplatsch.processor.base import MessageProcessor


class HealthCheckProcessor(MessageProcessor):

    def create_handle_record(self, data):
        record = {}
        return record

    def validate_handle_record(self, record):
        title = record.get("TITLE") or ""
        if len(title) < 3:
            return False
        return True
