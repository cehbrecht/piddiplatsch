import copy
import json
from piddiplatsch.handler import get_handler
from jsonschema.exceptions import ValidationError

import pytest

TEST_FILE_1 = {
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

TEST_DATASET_1 = {
    "handle": "21.t14996/testcase200",
    "aggregation_level": "DATASET",
    "operation": "publish",
    "is_replica": False,
    "version_number": 2016,
    "drs_id": "foo/bar/baz/drs/tc200",
    "files": ["hdl:21.t14996/snake", "hdl:21.t14996/monkey"],
    "message_timestamp": "2000-10-10T10:00:00.000000+00:00",
}


def test_map_file():
    handler = get_handler("cmip6")
    record = handler.map(TEST_FILE_1)
    assert record["AGGREGATION_LEVEL"] == "FILE"


def test_map_file_missing_file_name():
    handler = get_handler("cmip6")
    data = copy.deepcopy(TEST_FILE_1)
    del data["file_name"]

    with pytest.raises(ValidationError) as excinfo:
        handler.map(data)
    assert "'FILE_NAME' is a required property" in str(excinfo.value)


def test_map_dataset():
    handler = get_handler("cmip6")
    record = handler.map(TEST_DATASET_1)
    assert record["AGGREGATION_LEVEL"] == "DATASET"


def test_map_dataset_missing_drs_id():
    handler = get_handler("cmip6")
    data = copy.deepcopy(TEST_DATASET_1)
    del data["drs_id"]

    with pytest.raises(ValidationError) as excinfo:
        handler.map(data)
    assert "'DRS_ID' is a required property" in str(excinfo.value)


def test_process_message_dataset():
    handler = get_handler("cmip6")
    msg = json.dumps(TEST_FILE_1)
    handler.process_message(msg, dry_run=True)
