from piddiplatsch.handler.base import MessageHandler

import logging

LOGGER = logging.getLogger("piddiplatsch")


class WDCCHandler(MessageHandler):
    def configure(self):
        self._identifier = "wdcc"
        self._prefix = "21.14106"
        self._binding_key = "wdcc.#"

    def map(self, handle, data):
        record = {
            "URL": data.get("url_landing_page"),
            "AGGREGATION_LEVEL": data.get("aggregation_level"),
            "PUBLISHER": data.get("publisher"),
            "IS_PART_OF": data.get("is_part_of"),
            "TITLE": data.get("title"),
            "ENTRY_ID": data.get("entry_id"),
        }
        # TODO: handle flags like
        # message_json['please_allow_datasets_without_parents']
        return record

    def run_checks(self, handle, record):
        self.check_parent(handle, record)

    def check_parent(self, handle, record):
        parent = record.get("IS_PART_OF")
        if not parent:
            agg_level = record["AGGREGATION_LEVEL"]
            if agg_level == "dataset":
                msg = f'Handle {handle}: "is_part_of" is empty. Entities of type "dataset" must have a parent!'
                LOGGER.error(msg)
                raise ValueError(msg)
        else:
            ok = self.pid_maker.check_if_handle_exists(parent)
            if not ok:
                if parent.startswith("doi:"):
                    msg = f'Handle {handle}: Parent is a doi, but does not exist: "{parent}".'
                    LOGGER.error(msg)
                    raise ValueError(msg)
                elif parent.startswith("hdl:"):
                    msg = f'Handle {handle}: Parent is a handle and does not exist (yet?): "{parent}".'
                    LOGGER.warn(msg)
