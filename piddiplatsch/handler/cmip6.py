from piddiplatsch.handler.base import MessageHandler
from piddiplatsch.tools import map


class CMIP6Handler(MessageHandler):

    def configure(self):
        self._identifier = "cmip6"
        self._prefix = "21.14100"
        self._binding_key = "cmip6.#"

    def map(self, data):
        handle = map.get_handle(data, self.prefix)
        record = {
            "HANDLE": handle,
            "URL": f"https://handle-esgf.dkrz.de/lp/{handle}",
            "FIXED_CONTENT": data.get("fixed_content"),
            "AGGREGATION_LEVEL": data.get("aggregation_level"),
            "FILE_NAME": data.get("file_name"),
            "FILE_SIZE": data.get("file_size"),
            "IS_PART_OF": data.get("is_part_of"),
            "FILE_VERSION": data.get("file_version"),
            "CHECKSUM": data.get("checksum"),
            "CHECKSUM_METHOD": data.get("checksum_method"),
            "URL_ORIGINAL_DATA": data.get("url_original_data"),
            "URL_REPLICA": data.get("url_replica"),
            "DRS_ID": data.get("drs_id"),
            "VERSION_NUMBER": data.get("version_number"),
            "HAS_PARTS": data.get("has_parts"),
        }
        # remove empty values
        for key in list(record.keys()):
            value = record[key]
            if not value:
                del record[key]
        return record
