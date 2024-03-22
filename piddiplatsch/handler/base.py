import json
from pathlib import Path
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from dataclasses_json import Undefined
from piddiplatsch.pidmaker import PidMaker
from piddiplatsch.validator import validate

import logging

LOGGER = logging.getLogger("piddiplatsch")


def clean(record):
    # remove empty values
    for key in list(record.keys()):
        value = record[key]
        if not value:
            del record[key]
    return record


# HINT: see dataclasses usage.
# * https://docs.python.org/3/library/dataclasses.html
# * https://pypi.org/project/dataclasses-json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Options:
    allow_no_parent: bool = field(
        metadata=config(field_name="please_allow_datasets_without_parents"),
        default=False,
    )


class MessageHandler:
    def __init__(self) -> None:
        self.pid_maker = PidMaker()
        self._identifier = None
        self._prefix = None
        self._binding_key = None
        self._schema = None
        self._checker = None
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

    def process_message(self, message, dry_run=False):
        LOGGER.info(f"We got a message: {message}")
        data = json.loads(message)
        record = self.map_and_validate(data)
        self.publish(record, dry_run)

    def map_and_validate(self, data, options=None):
        options = Options.from_dict(data)
        record = self.map(data)
        record = clean(record)
        self.validate(record)
        self.check(record, options)
        return record

    def map(self, data):
        raise NotImplementedError

    def validate(self, record):
        validate(record, schema=self.schema)

    def check(self, record, options):
        if self._checker:
            self._checker.run_checks(record, options)

    def publish(self, record, dry_run=False):
        handle = record.get("HANDLE")
        if dry_run is True:
            LOGGER.warning(
                f"skip publishing (dry-run): handle={handle}, record={record}."
            )
        else:
            self.pid_maker.create_handle(handle, record)
