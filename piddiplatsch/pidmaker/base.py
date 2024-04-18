class BaseClient:
    def register_handle(self, handle, record):
        raise NotImplementedError

    def check_if_handle_exists(self, handle):
        raise NotImplementedError
