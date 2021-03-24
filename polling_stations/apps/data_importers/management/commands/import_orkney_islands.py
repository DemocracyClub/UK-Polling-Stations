from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ORK"
    addresses_name = (
        "2021-03-23T12:13:35.698255/Orkney polling_station_export-2021-03-23.csv"
    )
    stations_name = (
        "2021-03-23T12:13:35.698255/Orkney polling_station_export-2021-03-23.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
