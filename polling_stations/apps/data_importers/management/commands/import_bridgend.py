from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BGE"
    addresses_name = "2022-05-05/2022-03-29T11:07:35.962819/polling_station_export-2022-03-29.csv"
    stations_name = "2022-05-05/2022-03-29T11:07:35.962819/polling_station_export-2022-03-29.csv"
    elections = ['2022-05-05']
