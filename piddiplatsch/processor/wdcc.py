from piddiplatsch.processor.base import MessageProcessor


KERNEL_INFORMATION_PROFILE = (
    "https://redmine.dkrz.de/projects/handle/wiki/PID_profile_wdcc_doku#TEST_20220523"
)


class WDCCProcessor(MessageProcessor):

    def create_handle_record(self, data):
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

    def validate_handle_record(self, record):
        title = record.get("TITLE") or ""
        if len(title) < 3:
            return False
        return True
