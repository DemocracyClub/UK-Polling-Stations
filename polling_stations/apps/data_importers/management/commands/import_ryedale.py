from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RYE"
    addresses_name = "2022-05-05/2022-05-05T16:25:57.178337/polling_station_export-2022-05-05.csv"
    stations_name = "2022-05-05/2022-05-05T16:25:57.178337/polling_station_export-2022-05-05.csv"
    elections = ['2022-05-05']
