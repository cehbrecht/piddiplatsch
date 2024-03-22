import json
import copy
from piddiplatsch.handler import get_handler
from piddiplatsch.exceptions import CheckError
from jsonschema.exceptions import ValidationError

import pytest


@pytest.fixture
def data():
    _data = {
        "handle": "hdl:21.14106/test_abc_1",
        "url_landing_page": "https://www.wdc-climate.de/ui/entry?acronym=temperature",
        "is_part_of": "hdl:21.14106/test_temperature",
        "publisher": "WDCC at DKRZ",
        "aggregation_level": "dataset",
        "title": "temperature",
        "entry_id": "2426195",
        "please_allow_datasets_without_parents": False,
    }
    return copy.deepcopy(_data)


def test_map(data):
    handler = get_handler("wdcc")
    record = handler.map_and_validate(data)
    assert record["AGGREGATION_LEVEL"] == "dataset"


def test_map_missing_required_fields(data):
    handler = get_handler("wdcc")
    for field in [
        "url_landing_page",
        "aggregation_level",
        "title",
        "entry_id",
        "publisher",
    ]:
        del data[field]
        with pytest.raises(ValidationError) as excinfo:
            handler.map_and_validate(data)
        assert "is a required property" in str(excinfo.value)


def test_map_invalid_handle(data):
    handler = get_handler("wdcc")
    data["handle"] = "invalid_handle"
    with pytest.raises(ValidationError) as excinfo:
        handler.map_and_validate(data)
    assert "'invalid_handle' is not a 'handle'" in str(excinfo.value)


def test_map_invalid_parent(data):
    handler = get_handler("wdcc")
    data["is_part_of"] = "doi:10.1001/invalid"
    with pytest.raises(CheckError) as excinfo:
        handler.map_and_validate(data)
    assert "Parent is a doi, but does not exist" in str(excinfo.value)


def test_map_invalid_parent_with_option(data):
    handler = get_handler("wdcc")
    data["is_part_of"] = "doi:10.1001/invalid"
    data["please_allow_datasets_without_parents"] = True
    record = handler.map_and_validate(data)
    assert record["AGGREGATION_LEVEL"] == "dataset"


def test_map_missing_parent(data):
    handler = get_handler("wdcc")
    del data["is_part_of"]
    with pytest.raises(ValidationError) as excinfo:
        handler.map_and_validate(data)
    assert "'IS_PART_OF' is a required property" in str(excinfo.value)


def test_process_message(data):
    handler = get_handler("wdcc")
    msg = json.dumps(data)
    handler.process_message(msg, dry_run=True)
