from piddiplatsch.handler.wdcc import WDCCHandler
from piddiplatsch.handler.cmip6 import CMIP6Handler


HANDLERS = [WDCCHandler(), CMIP6Handler()]


def all_handlers():
    return HANDLERS


def filter_handlers(handlers):
    if "all" in handlers:
        return all_handlers()
    enabled = []
    for h in all_handlers():
        if h.identifier in handlers:
            enabled.append(h)
    return enabled
