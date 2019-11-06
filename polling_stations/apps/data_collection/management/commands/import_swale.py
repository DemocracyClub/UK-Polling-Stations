from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000113"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-04swale.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-04swale.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False
