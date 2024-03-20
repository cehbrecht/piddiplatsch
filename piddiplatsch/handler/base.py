import json
import uuid
from pathlib import Path
from jsonschema import validate
from jsonschema import Draft202012Validator
import pyhandle
from piddiplatsch.pidmaker import PidMaker

import logging

LOGGER = logging.getLogger("piddiplatsch")


class MessageHandler:
    def __init__(self) -> None:
        self.pid_maker = PidMaker()
        self._identifier = None
        self._prefix = None
        self._binding_key = None
        self._schema = None
        self.configure()

    def configure(self):
        raise NotImplementedError

    @property
    def identifier(self):
        return self._identifier

    @property
    def prefix(self):
        return self._prefix

    @property
    def queue_name(self):
        return f"queue_{self.binding_key}"

    @property
    def binding_key(self):
        return self._binding_key

    @property
    def schema(self):
        if not self._schema:
            self.load_schema()
        return self._schema

    def load_schema(self):
        schema_path = (
            Path(__file__).parent.parent.parent / "schema" / f"{self.identifier}.json"
        )
        with open(schema_path) as schema_file:
            self._schema = json.load(schema_file)

    def on_message(self, ch, method, properties, body):
        LOGGER.info(f"consume routing key: {method.routing_key}")
        try:
            self.process_message(body)
        except Exception:
            LOGGER.exception("message processing failed")
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def process_message(self, message):
        data = json.loads(message)
        LOGGER.info(f"We got a message: {data}")
        handle = self.get_handle(data)
        self.validate_handle(handle)
        record = self.map(handle, data)
        self.validate(record)
        self.run_checks(handle, record)
        self.pid_maker.create_handle(handle, record)

    def get_handle(self, data):
        if "handle" in data:
            handle = data.get("handle")
            handle = handle.lstrip("hdl:")
        else:
            handle = self.generate_handle()
        return handle

    def generate_handle(self, suffix=None):
        if not suffix:
            suffix = str(uuid.uuid4())
        handle = f"{self.prefix}/{suffix}"
        return handle

    def validate_handle(self, handle):
        pyhandle.utilhandle.check_handle_syntax(handle)

    def map(self, handle, data):
        raise NotImplementedError

    def validate(self, record):
        validate(
            record,
            schema=self.schema,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )

    def run_checks(self, handle, record):
        pass
