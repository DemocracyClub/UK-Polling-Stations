from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NTL"
    addresses_name = (
        "2022-06-23/2022-05-19T13:53:39.766566/polling_station_export-2021-12-17.csv"
    )
    stations_name = (
        "2022-06-23/2022-05-19T13:53:39.766566/polling_station_export-2021-12-17.csv"
    )
    elections = ["2022-06-23"]
