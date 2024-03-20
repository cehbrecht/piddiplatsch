from piddiplatsch.handler.wdcc import WDCCHandler
from piddiplatsch.handler.cmip6 import CMIP6Handler


HANDLERS = [WDCCHandler(), CMIP6Handler()]


def all_handlers():
    return HANDLERS


def filter_handlers(handlers):
    # compare lowercase
    handlers = [h.lower() for h in handlers]
    # enable all handlers?
    if "all" in handlers:
        return all_handlers()
    # enable selected handlers
    enabled = []
    for h in all_handlers():
        if h.identifier.lower() in handlers:
            enabled.append(h)
    return enabled


def get_handler(identifier):
    handlers = filter_handlers([identifier])
    handler = None
    if len(handlers) == 1:
        handler = handlers[0]
    return handler
