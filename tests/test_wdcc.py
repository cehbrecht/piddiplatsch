import json
from piddiplatsch.handler import filter_handlers

TEST_1 = {
    "handle": "hdl:21.14106/test_abc1234",
    "url_landing_page": "https://www.wdc-climate.de/ui/entry?acronym=temperature",
    "is_part_of": "hdl:21.14106/test_temperature",
    "publisher": "WDCC at DKRZ",
    "aggregation_level": "dataset",
    "title": "temperature",
    "entry_id": "2426195",
    "please_allow_datasets_without_parents": False,
}


def test_map():
    handler = filter_handlers(["wdcc"])[0]
    record = handler.map(TEST_1)
    assert record["AGGREGATION_LEVEL"] == "dataset"


def test_process_message():
    handler = filter_handlers(["wdcc"])[0]
    msg = json.dumps(TEST_1)
    handler.process_message(msg, dry_run=True)
