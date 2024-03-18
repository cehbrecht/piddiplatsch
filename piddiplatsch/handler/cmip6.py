from piddiplatsch.handler.base import MessageHandler

AGGREGATION_LEVELS = ["FILE", "DATASET"]
CHECKSUM_METHODS = ["MD5", "SHA256"]


SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "WDCC",
    "description": "A handle record schema for WDCC.",
    "type": "object",
    "properties": {
        "HANDLE": {
            "description": "Handle identifier. Example: 21.T14996/TESTCASE100",
            "type": "string",
        },
        "AGGREGATION_LEVEL": {"enum": AGGREGATION_LEVELS},
        "FILE_NAME": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200,
        },
        "FILE_SIZE": {
            "type": "integer",
            "minimum": 0,
        },
        "FILE_VERSION": {
            "type": "integer",
            "minimum": 0,
        },
        "CHECKSUM": {"type": "string"},
        "CHECKSUM_METHOD": {"enum": CHECKSUM_METHODS},
        "FIXED_CONTENT": {"type": "boolean"},
        "URL": {
            "description": "URL of the landing page",
            "type": "string",
            "format": "uri",
        },
        "URL_ORIGINAL_DATA": {
            "type": "string",
            "format": "uri",
        },
        "URL_REPLICA": {
            "type": "string",
            "format": "uri",
        },
        "IS_PART_OF": {
            "type": "string",
            "format": "uri",
        },
        "DRS_ID": {
            "type": "string",
        },
        "VERSION_NUMBER": {
            "type": "string",
        },
        "HOSTING_NODE": {
            "type": "string",
        },
        "REPLICA_NODE": {
            "type": "string",
        },
        "HAS_PARTS": {
            "type": "string",
        },
        "REPLACES": {
            "type": "string",
        },
        "REPLACED_BY": {
            "type": "string",
        },
    },
    "required": ["URL", "AGGREGATION_LEVEL", "FILE_NAME"],
}


class CMIP6Handler(MessageHandler):

    def configure(self):
        self._identifier = "cmip6"
        self._prefix = "21.14100"
        self._binding_key = "cmip6.#"
        self._schema = SCHEMA

    def map(self, handle, data):
        record = {
            "URL": f"https://handle-esgf.dkrz.de/lp/{handle}",
            "AGGREGATION_LEVEL": data.get("aggregation_level"),
            "FILE_NAME": data.get("file_name"),
            "FILE_SIZE": data.get("file_size"),
            "IS_PART_OF": data.get("is_part_of"),
            "FILE_VERSION": data.get("file_version"),
            "CHECKSUM": data.get("checksum"),
            "CHECKSUM_METHOD": data.get("checksum_method"),
            "URL_ORIGINAL_DATA": data.get("url_original_data"),
            "URL_REPLICA": data.get("url_replica"),
        }
        return record
