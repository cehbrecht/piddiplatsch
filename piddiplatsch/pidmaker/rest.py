from .base import BaseClient

import pyhandle


class RESTClient(BaseClient):
    def __init__(self):
        self.client = pyhandle.handleclient.PyHandleClient("rest")

    def register_handle(self, handle, record):
        self.client.register_handle(handle, record)

    def check_if_handle_exists(self, handle):
        return self.client.check_if_handle_exists(handle)
