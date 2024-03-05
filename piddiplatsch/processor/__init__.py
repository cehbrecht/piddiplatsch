from piddiplatsch.processor.wdcc import WDCCProcessor


def get_message_processor(name):
    if name == "cmip6":
        pass
    else:
        p = WDCCProcessor()
    return p
