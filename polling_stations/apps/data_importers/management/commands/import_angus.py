from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ANS"
    addresses_name = "2022-05-05/2022-02-11T11:29:59.770553/polling_station_export-2022-02-03.csv"
    stations_name = "2022-05-05/2022-02-11T11:29:59.770553/polling_station_export-2022-02-03.csv"
    elections = ['2022-05-05']
