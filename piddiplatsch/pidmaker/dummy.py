from .base import BaseClient

import logging

LOGGER = logging.getLogger("piddiplatsch")


class DummyClient(BaseClient):
    def register_handle(self, handle, record):
        LOGGER.info(f"handle: {handle}")
        LOGGER.info(f"record: {record}")

    def check_if_handle_exists(self, handle):
        if not handle:
            return False
        elif "invalid" in handle:
            return False
        return True
