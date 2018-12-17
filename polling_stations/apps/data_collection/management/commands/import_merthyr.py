from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "W06000024"
    addresses_name = (
        "parl.2017-06-08/Version 1/Merthyr Tydfil polling_station_export-2017-05-25.csv"
    )
    stations_name = (
        "parl.2017-06-08/Version 1/Merthyr Tydfil polling_station_export-2017-05-25.csv"
    )
    elections = ["parl.2017-06-08"]
    csv_encoding = "latin-1"
