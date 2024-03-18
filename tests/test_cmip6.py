import json
from piddiplatsch.handler import filter_handlers


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
