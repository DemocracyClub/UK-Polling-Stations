from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000001"
    addresses_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-06.csv"
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-06.csv"
    elections = ["parl.2019-12-12"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.housepostcode == "EC4Y 9BE":
            return None

        return rec
