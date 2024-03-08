from piddiplatsch.processor.wdcc import WDCCProcessor


def get_message_processor(name):
    if name == "wdcc":
        p = WDCCProcessor()
    else:
        raise ValueError(f"consumer type {name} is not known.")
    return p
