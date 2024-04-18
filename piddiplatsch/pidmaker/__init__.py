from .rest import RESTClient
from .dummy import DummyClient


def PidMaker(dry_run=True):
    if dry_run:
        client = DummyClient()
    else:
        client = RESTClient()
    return client
