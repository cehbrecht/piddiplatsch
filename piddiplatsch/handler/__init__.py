from piddiplatsch.handler.wdcc import WDCCHandler
from piddiplatsch.handler.cmip6 import CMIP6Handler


HANDLERS = [WDCCHandler(), CMIP6Handler()]


def all_handlers():
    return HANDLERS
