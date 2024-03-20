from piddiplatsch.handler import filter_handlers


def test_wdcc_map_file():
    handler = filter_handlers(["wdcc"])[0]
    data = {
        "handle": "hdl:21.14106/test_abc1234",
        "url_landing_page": "https://www.wdc-climate.de/ui/entry?acronym=temperature",
        "is_part_of": "hdl:21.14106/test_temperature",
        "publisher": "WDCC at DKRZ",
        "aggregation_level": "dataset",
        "title": "temperature",
        "entry_id": "2426195",
        "please_allow_datasets_without_parents": False,
    }
    record = handler.map(data)
    assert record["AGGREGATION_LEVEL"] == "dataset"
