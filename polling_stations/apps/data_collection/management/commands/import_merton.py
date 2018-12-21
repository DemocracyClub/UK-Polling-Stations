from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000024"
    addresses_name = "local.2018-05-03/Version 1/polling_station_export-2018-04-16.csv"
    stations_name = "local.2018-05-03/Version 1/polling_station_export-2018-04-16.csv"
    elections = ["local.2018-05-03"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.housepostcode == "CR4 4JA":
            return None

        if record.houseid == "30851":
            return None

        return super().address_record_to_dict(record)
