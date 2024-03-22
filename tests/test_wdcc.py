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


@pytest.fixture
def handler():
    handler = get_handler("wdcc")
    handler.dry_run = True
    return handler


def test_map(handler, data):
    record = handler.map_and_validate(data)
    assert record["AGGREGATION_LEVEL"] == "dataset"


def test_map_missing_required_fields(handler, data):
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


def test_map_invalid_handle(handler, data):
    data["handle"] = "invalid_handle"
    with pytest.raises(ValidationError) as excinfo:
        handler.map_and_validate(data)
    assert "'invalid_handle' is not a 'handle'" in str(excinfo.value)


def test_map_invalid_parent(handler, data):
    data["is_part_of"] = "doi:10.1001/invalid"
    data["please_allow_datasets_without_parents"] = False
    with pytest.raises(CheckError) as excinfo:
        handler.map_and_validate(data)
    assert "Parent is a doi, but does not exist" in str(excinfo.value)


def test_map_invalid_parent_with_option(handler, data):
    data["is_part_of"] = "doi:10.1001/invalid"
    data["please_allow_datasets_without_parents"] = True
    record = handler.map_and_validate(data)
    assert record["AGGREGATION_LEVEL"] == "dataset"


def test_map_missing_parent(handler, data):
    del data["is_part_of"]
    with pytest.raises(ValidationError) as excinfo:
        handler.map_and_validate(data)
    assert "'IS_PART_OF' is a required property" in str(excinfo.value)


def test_process_message(handler, data):
    msg = json.dumps(data)
    handler.process_message(msg)
