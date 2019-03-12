from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000215"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-28tandb.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-28tandb.csv"
    )
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.houseid == "37666":
            rec["accept_suggestion"] = True
        if record.houseid == "37412":
            rec["accept_suggestion"] = False

        if record.houseid in ["8211", "8212"]:
            rec["accept_suggestion"] = False

        return rec
