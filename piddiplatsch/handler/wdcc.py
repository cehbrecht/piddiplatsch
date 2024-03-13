from piddiplatsch.handler.base import MessageHandler


KERNEL_INFORMATION_PROFILE = (
    "https://redmine.dkrz.de/projects/handle/wiki/PID_profile_wdcc_doku#TEST_20220523"
)


class WDCCHandler(MessageHandler):
    def configure(self):
        self._prefix = "21.14106"
        self._binding_key = "wdcc.#"

    def create_handle_record(self, handle, data):
        # http://fox.cloud.dkrz.de:8006/api/handles/21.14106/81D6053E36D55F4D41C1E5757684A35BB9BCEB0F
        record = {
            "URL": "https://www.wdc-climate.de/ui/entry?acronym=MXELv6MOOrsntds111v120627",
            "AGGREGATION_LEVEL": "dataset",
            "PUBLISHER": "WDCC at DKRZ",
            "IS_PART_OF": "doi:10.1594/WDCC/CMIP5.MXELv6",
            "TITLE": data.get("title"),
            "ENTRY_ID": "2426195",
            "KERNEL_INFORMATION_PROFILE": KERNEL_INFORMATION_PROFILE,
        }
        return record

    def validate(self, handle, record):
        if not handle.startswith(self.prefix):
            return False
        title = record.get("TITLE") or ""
        if len(title) < 3:
            return False
        return True
