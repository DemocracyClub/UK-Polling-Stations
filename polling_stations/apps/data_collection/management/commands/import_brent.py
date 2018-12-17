from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000005"
    addresses_name = (
        "local.2018-05-03/Version 1/polling_station_export-2018-02-20 Brent.csv"
    )
    stations_name = (
        "local.2018-05-03/Version 1/polling_station_export-2018-02-20 Brent.csv"
    )
    elections = ["local.2018-05-03"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.housepostcode == "NW9 9LY":
            return None
        if record.houseid == "122323":
            return None
        if record.housepostcode == "NW10 7RT":
            return None
        if record.houseid == "129088":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "HA0 2TG"
            return rec

        return super().address_record_to_dict(record)
