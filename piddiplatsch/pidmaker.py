import pyhandle


import logging

LOGGER = logging.getLogger("piddiplatsch")


class PidMaker:

    def __init__(self):
        self.client = DummyClient()

    def create_handle(self, handle, record):
        self.client.register_handle(handle, record)
        return True


class BaseClient:
    def register_handle(self, handle, record):
        raise NotImplementedError


class DummyClient(BaseClient):
    def register_handle(self, handle, record):
        LOGGER.info(f"handle: {handle}")
        LOGGER.info(f"record: {record}")


class RealClient(BaseClient):
    def __init__(self):
        self.client = pyhandle.handleclient.PyHandleClient("rest")

    def register_handle(self, handle, record):
        self.client.register_handle(handle, record)
