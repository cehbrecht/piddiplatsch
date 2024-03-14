from piddiplatsch.handler.base import MessageHandler


KERNEL_INFORMATION_PROFILE = (
    "https://redmine.dkrz.de/projects/handle/wiki/PID_profile_wdcc_doku#TEST_20220523"
)

AGGREGATION_LEVELS = ["dataset", "dataset_collection"]
PUBLISHERS = ["WDCC at DKRZ", "DOKU at DKRZ"]

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "WDCC",
    "description": "A handle record schema for WDCC.",
    "type": "object",
    "properties": {
        "URL": {
            "description": "URL of the landing page",
            "type": "string",
            "format": "uri",
        },
        "AGGREGATION_LEVEL": {
            "description": "Type of entity.",
            "enum": AGGREGATION_LEVELS,
        },
        "PUBLISHER": {"enum": PUBLISHERS},
        "TITLE": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1000,
        },
        "ENTRY_ID": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200,
        },
        "IS_PART_OF": {
            "type": "string",
            "format": "uri",
        },
        "KERNEL_INFORMATION_PROFILE": {
            "type": "string",
            "format": "uri",
        },
    },
    "required": ["URL", "AGGREGATION_LEVEL", "PUBLISHER", "TITLE", "ENTRY_ID"],
}


class WDCCHandler(MessageHandler):
    def configure(self):
        self._identifier = "wdcc"
        self._prefix = "21.14106"
        self._binding_key = "wdcc.#"
        self._schema = SCHEMA

    def create_handle_record(self, handle, data):
        # http://fox.cloud.dkrz.de:8006/api/handles/21.14106/81D6053E36D55F4D41C1E5757684A35BB9BCEB0F
        record = {
            "URL": "https://www.wdc-climate.de/ui/entry?acronym=MXELv6MOOrsntds111v120627",
            "AGGREGATION_LEVEL": data.get("aggregation_level") or "dataset",
            "PUBLISHER": "WDCC at DKRZ",
            "IS_PART_OF": "doi:10.1594/WDCC/CMIP5.MXELv6",
            "TITLE": data.get("title"),
            "ENTRY_ID": "2426195",
            "KERNEL_INFORMATION_PROFILE": KERNEL_INFORMATION_PROFILE,
        }
        return record
