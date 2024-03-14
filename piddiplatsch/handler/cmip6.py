from piddiplatsch.handler.base import MessageHandler

AGGREGATION_LEVELS = ["FILE", "DATASET"]

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "WDCC",
    "description": "A handle record schema for WDCC.",
    "type": "object",
    "properties": {
        "URL": {
            "description": "URL of the landing page",
            "type": "string",
            "format": "uri",
        },
        "AGGREGATION_LEVEL": {"enum": AGGREGATION_LEVELS},
        "FILE_NAME": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200,
        },
        "FILE_SIZE": {
            "type": "integer",
            "minimum": 0,
        },
        "FILE_VERSION": {
            "type": "integer",
            "minimum": 0,
        },
        "CHECKSUM": {"type": "string"},
        "CHECKSUM_METHOD": {"type": "string"},
        "URL_ORIGINAL_DATA": {
            "type": "string",
            "format": "uri",
        },
        "URL_REPLICA": {
            "type": "string",
            "format": "uri",
        },
        "IS_PART_OF": {
            "type": "string",
            "format": "uri",
        },
    },
    "required": ["URL", "AGGREGATION_LEVEL", "FILE_NAME"],
}


class CMIP6Handler(MessageHandler):

    def configure(self):
        self._identifier = "cmip6"
        self._prefix = "21.14100"
        self._binding_key = "cmip6.#"
        self._schema = SCHEMA

    def create_handle_record(self, handle, data):
        # http://fox.cloud.dkrz.de:8000/api/handles/21.14100/77b13123-f172-483c-a53b-2ee7686aa437
        record = {
            "URL": f"https://handle-esgf.dkrz.de/lp/{handle}",
            "AGGREGATION_LEVEL": data.get("aggregation_level") or "FILE",
            # "FILE_NAME": "wap_Eday_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_18500101-18891231.nc",
            "FILE_NAME": data.get("file_name"),
            # "FILE_SIZE": "18028171468",
            # "IS_PART_OF": "hdl:21.14100/37528ff1-2653-3c50-b670-7c00ba96fd6e",
            "FILE_VERSION": 1,
            # "CHECKSUM": "312cb59854334b340d4d046310d028d08e0e71cfaa31ac031b383e1008594d42",
            # "CHECKSUM_METHOD": "SHA256",
            # "URL_ORIGINAL_DATA": "http://vesg.ipsl.upmc.fr/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Eday/wap/gr/v20180727/wap_Eday_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_18500101-18891231.nc",
            # "URL_REPLICA": "http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/IPSL/IPSL-CM6A-LR/1pctCO2/r1i1p1f1/Eday/wap/gr/v20180727/wap_Eday_IPSL-CM6A-LR_1pctCO2_r1i1p1f1_gr_18500101-18891231.nc",
        }
        return record
