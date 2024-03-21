import json
import copy
from piddiplatsch.handler import get_handler
from jsonschema.exceptions import ValidationError

import pytest

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
    handler = get_handler("wdcc")
    record = handler.map(TEST_1)
    assert record["AGGREGATION_LEVEL"] == "dataset"


def test_map_required_fields():
    handler = get_handler("wdcc")
    data = copy.deepcopy(TEST_1)
    del data["aggregation_level"]
    with pytest.raises(ValidationError) as excinfo:
        handler.map(data)
    assert "'AGGREGATION_LEVEL' is a required property" in str(excinfo.value)


def test_map_invalid_handle():
    handler = get_handler("wdcc")
    data = copy.deepcopy(TEST_1)
    data["handle"] = "invalid_handle"
    with pytest.raises(ValidationError) as excinfo:
        handler.map(data)
    assert "'invalid_handle' is not a 'handle'" in str(excinfo.value)


def test_process_message():
    handler = get_handler("wdcc")
    msg = json.dumps(TEST_1)
    handler.process_message(msg, dry_run=True)
