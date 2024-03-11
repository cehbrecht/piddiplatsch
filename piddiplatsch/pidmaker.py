import pyhandle


class PidMaker:

    def __init__(self):
        self.client = DummyClient()

    def create_handle(self, handle, record):
        self.client.register_handle(handle, record)


class BaseClient:
    def register_handle(self):
        pass


class DummyClient:
    def register_handle(self):
        pass


class RealClient:
    def __init__(self):
        self.client = pyhandle.handleclient.PyHandleClient("rest")

    def register_handle(self):
        self.client.register_handle()
