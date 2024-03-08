from piddiplatsch.processor.wdcc import WDCCProcessor
from piddiplatsch.processor.cmip6 import CMIP6Processor


def get_message_processor(routing_key):
    if routing_key == "pids.wdcc":
        p = WDCCProcessor()
    elif routing_key == "pids.cmip6":
        p = CMIP6Processor()
    else:
        raise ValueError(f"consumer for {routing_key} is not known.")
    return p
