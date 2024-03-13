from piddiplatsch.handler.wdcc import WDCCHandler
from piddiplatsch.handler.cmip6 import CMIP6Handler


def all_message_handlers():
    handlers = [WDCCHandler(), CMIP6Handler()]
    return handlers
