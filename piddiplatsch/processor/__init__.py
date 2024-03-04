from piddiplatsch.processor.default import DefaultProcessor


def get_message_processor(name):
    if name == "cmip6":
        pass
    else:
        p = DefaultProcessor()
    return p
