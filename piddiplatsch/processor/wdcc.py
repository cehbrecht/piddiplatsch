from piddiplatsch.processor.base import MessageProcessor


KERNEL_INFORMATION_PROFILE = (
    "https://redmine.dkrz.de/projects/handle/wiki/PID_profile_wdcc_doku#TEST_20220523"
)


class WDCCProcessor(MessageProcessor):
    def do_process_message(self, data):
        print(f"We got a message: {data}")
        record = self.make_handle_record(data)
        print(record)

    def make_handle_record(self, data):
        # http://fox.cloud.dkrz.de:8006/api/handles/21.14106/81D6053E36D55F4D41C1E5757684A35BB9BCEB0F
        record = {
            "URL": "https://www.wdc-climate.de/ui/entry?acronym=MXELv6MOOrsntds111v120627",
            "AGGREGATION_LEVEL": "dataset",
            "PUBLISHER": "WDCC at DKRZ",
            "IS_PART_OF": "doi:10.1594/WDCC/CMIP5.MXELv6",
            "TITLE": "cmip5 output1 MPI-M MPI-ESM-LR noVolc1960 mon ocean Omon r1i1p1 v20120627 rsntds",
            "ENTRY_ID": "2426195",
            "KERNEL_INFORMATION_PROFILE": KERNEL_INFORMATION_PROFILE,
        }
        return record
