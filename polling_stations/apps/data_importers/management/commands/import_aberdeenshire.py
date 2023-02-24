from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABD"
    addresses_name = (
        "2023-02-23/2023-02-24T07:52:57.895726/polling_station_export-2023-02-23.csv"
    )
    stations_name = (
        "2023-02-23/2023-02-24T07:52:57.895726/polling_station_export-2023-02-23.csv"
    )
    elections = ["2023-02-23"]
