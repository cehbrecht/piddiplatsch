import json
from piddiplatsch.handler import filter_handlers
from jsonschema.exceptions import ValidationError

import pytest


def test_cmip6_map_file():
    handler = filter_handlers(["cmip6"])[0]
    msg = {
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
    data = json.dumps(msg)
    handler.process_message(data)


def test_cmip6_map_file_missing_file_name():
    handler = filter_handlers(["cmip6"])[0]
    msg = {
        "handle": "21.t14996/testcase100",
        "aggregation_level": "FILE",
        "operation": "publish",
        "is_replica": False,
        # "file_name": "temperature.nc",
        "file_size": 1000,
        "checksum": "ch123abc",
        "checksum_method": "MD5",
        "url_original_data": "https://dkrz.de/baz/temperature.nc",
        "file_version": 1,
        "message_timestamp": "2000-10-10T10:00:00.000000+00:00",
        "parent_dataset": "hdl:21.t14996/cucumber",
    }
    data = json.dumps(msg)

    with pytest.raises(ValidationError) as excinfo:
        handler.process_message(data)
    assert "'FILE_NAME' is a required property" in str(excinfo.value)


def test_cmip6_map_dataset():
    handler = filter_handlers(["cmip6"])[0]
    msg = {
        "handle": "21.t14996/testcase200",
        "aggregation_level": "DATASET",
        "operation": "publish",
        "is_replica": False,
        "version_number": 2016,
        "drs_id": "foo/bar/baz/drs/tc200",
        "files": ["hdl:21.t14996/snake", "hdl:21.t14996/monkey"],
        "message_timestamp": "2000-10-10T10:00:00.000000+00:00",
    }
    data = json.dumps(msg)
    handler.process_message(data)


def test_cmip6_map_dataset_missing_drs_id():
    handler = filter_handlers(["cmip6"])[0]
    msg = {
        "handle": "21.t14996/testcase200",
        "aggregation_level": "DATASET",
        "operation": "publish",
        "is_replica": False,
        "version_number": 2016,
        # "drs_id": "foo/bar/baz/drs/tc200",
        "files": ["hdl:21.t14996/snake", "hdl:21.t14996/monkey"],
        "message_timestamp": "2000-10-10T10:00:00.000000+00:00",
    }
    data = json.dumps(msg)

    with pytest.raises(ValidationError) as excinfo:
        handler.process_message(data)
    assert "'DRS_ID' is a required property" in str(excinfo.value)
