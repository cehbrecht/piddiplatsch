import pyhandle


import logging

LOGGER = logging.getLogger("piddiplatsch")


class PidMaker:

    def __init__(self):
        self.client = DummyClient()

    def create_handle(self, handle, record):
        self.client.register_handle(handle, record)
        return True

    def check_if_handle_exists(self, handle):
        return self.client.check_if_handle_exists(handle)


class BaseClient:
    def register_handle(self, handle, record):
        raise NotImplementedError

    def check_if_handle_exists(self, handle):
        raise NotImplementedError


class DummyClient(BaseClient):
    def register_handle(self, handle, record):
        LOGGER.info(f"handle: {handle}")
        LOGGER.info(f"record: {record}")

    def check_if_handle_exists(self, handle):
        LOGGER.info(f"handle exists: {handle}")
        return True


class RESTClient(BaseClient):
    def __init__(self):
        self.client = pyhandle.handleclient.PyHandleClient("rest")

    def register_handle(self, handle, record):
        self.client.register_handle(handle, record)

    def check_if_handle_exists(self, handle):
        return self.client.check_if_handle_exists(handle)
