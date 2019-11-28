from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E06000017"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-13rut.csv"
    )
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-13rut.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.housepostcode == "PE9 4EG":

            return None

        return rec
