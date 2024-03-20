import json
from piddiplatsch.handler import filter_handlers


def test_wdcc_map_file():
    handler = filter_handlers(["wdcc"])[0]
    msg = {
        # "handle": handle,
        "url_landing_page": "https://www.wdc-climate.de/ui/entry?acronym=temperature",
        "is_part_of": "hdl:21.14106/test_temperature",
        "publisher": "WDCC at DKRZ",
        "aggregation_level": "dataset",
        "title": "temperature",
        "entry_id": "2426195",
        "please_allow_datasets_without_parents": False,
    }
    data = json.dumps(msg)
    handler.process_message(data)
