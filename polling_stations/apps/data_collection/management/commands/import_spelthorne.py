from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000213"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export Spelthorne-2019-02-07.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export Spelthorne-2019-02-07.csv"
    )
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):

        if record.houseid == "43674":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TW15 2SH"
            return rec

        return super().address_record_to_dict(record)
