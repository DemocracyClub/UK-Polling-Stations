from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABD"
    addresses_name = "2026-07-02/2026-05-28T10:39:21.202438/Aberdeenshire Ward 6_Democracy Club - Idox_2026-05-26 10-20.csv"
    stations_name = "2026-07-02/2026-05-28T10:39:21.202438/Aberdeenshire Ward 6_Democracy Club - Idox_2026-05-26 10-20.csv"
    elections = ["2026-07-02"]

    # maintaining correction through by-election
    # def station_record_to_dict(self, record):
    #     # corrects wrong postcode for: TOWIE PUBLIC HALL, TOWIE, GLENKINDIE, ALFORD AB33 8NR
    #     if self.get_station_hash(record) == "44-towie-public-hall":
    #         record = record._replace(pollingstationpostcode="AB33 8RN")

    #     return super().station_record_to_dict(record)
