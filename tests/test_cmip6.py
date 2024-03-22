import copy
import json
from piddiplatsch.handler import get_handler
from jsonschema.exceptions import ValidationError

import pytest


@pytest.fixture
def data_file():
    _data = {
        "handle": "21.t14996/testcase100",
        "aggregation_level": "FILE",
        "operation": "publish",
        "is_replica": False,
        "file_name": "temperature.nc",
        "file_size": 1000,
        "checksum": "ch123abc",
        "checksum_method": "MD5",
        "url_original_data": "https://dkrz.de/baz/temperature.nc",
        "file_version": 1,
        "message_timestamp": "2000-10-10T10:00:00.000000+00:00",
        "parent_dataset": "hdl:21.t14996/cucumber",
    }
    return copy.deepcopy(_data)


@pytest.fixture
def data_dataset():
    _data = {
        "handle": "21.t14996/testcase200",
        "aggregation_level": "DATASET",
        "operation": "publish",
        "is_replica": False,
        "version_number": 2016,
        "drs_id": "foo/bar/baz/drs/tc200",
        "files": ["hdl:21.t14996/snake", "hdl:21.t14996/monkey"],
        "message_timestamp": "2000-10-10T10:00:00.000000+00:00",
    }
    return copy.deepcopy(_data)


@pytest.fixture
def handler():
    return get_handler("cmip6")


def test_map_file(handler, data_file):
    record = handler.map_and_validate(data_file)
    assert record["URL"] == "https://handle-esgf.dkrz.de/lp/21.t14996/testcase100"
    assert record["AGGREGATION_LEVEL"] == "FILE"


def test_map_file_missing_required_fields(handler, data_file):
    for field in ["aggregation_level", "file_name"]:
        data = copy.deepcopy(data_file)
        del data[field]

        with pytest.raises(ValidationError) as excinfo:
            handler.map_and_validate(data)
        assert "is a required property" in str(excinfo.value)


def test_map_dataset(handler, data_dataset):
    record = handler.map_and_validate(data_dataset)
    assert record["URL"] == "https://handle-esgf.dkrz.de/lp/21.t14996/testcase200"
    assert record["AGGREGATION_LEVEL"] == "DATASET"


def test_map_dataset_missing_required_fields(handler, data_dataset):
    for field in ["aggregation_level", "drs_id"]:
        data = copy.deepcopy(data_dataset)
        del data[field]

        with pytest.raises(ValidationError) as excinfo:
            handler.map_and_validate(data)
        assert "is a required property" in str(excinfo.value)


def test_process_message_dataset(handler, data_file):
    msg = json.dumps(data_file)
    handler.process_message(msg, dry_run=True)
