from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E06000019"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-19Here.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-19Here.csv"
    )
    elections = ["local.2019-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.housepostcode.strip() == "HR9 7RA":
            return None

        if record.houseid in ["9012185", "9012186"]:
            return None

        if record.houseid == "3072006":
            return None

        if record.housepostcode.strip() == "HR1 2PJ":
            return None

        return rec
