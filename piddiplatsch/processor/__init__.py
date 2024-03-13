from piddiplatsch.processor.wdcc import WDCCProcessor
from piddiplatsch.processor.cmip6 import CMIP6Processor


def all_message_consumers():
    consumers = [WDCCProcessor(), CMIP6Processor()]
    return consumers
