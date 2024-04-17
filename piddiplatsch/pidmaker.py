import pyhandle
import time


import logging

LOGGER = logging.getLogger("piddiplatsch")


def PidMaker(dry_run=True):
    if dry_run:
        client = DummyClient()
    else:
        client = RESTClient()
    return client


class BaseClient:
    def register_handle(self, handle, record):
        raise NotImplementedError

    def check_if_handle_exists(self, handle):
        raise NotImplementedError


class DummyClient(BaseClient):
    def register_handle(self, handle, record):
        LOGGER.info(f"handle: {handle}")
        LOGGER.info(f"record: {record}")
        time.sleep(1)

    def check_if_handle_exists(self, handle):
        if not handle:
            return False
        elif "invalid" in handle:
            return False
        return True


class RESTClient(BaseClient):
    def __init__(self):
        self.client = pyhandle.handleclient.PyHandleClient("rest")

    def register_handle(self, handle, record):
        self.client.register_handle(handle, record)

    def check_if_handle_exists(self, handle):
        return self.client.check_if_handle_exists(handle)
