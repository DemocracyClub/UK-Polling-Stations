from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = "2023-02-16/2023-01-16T16:13:21/Polling Districts.csv"
    stations_name = "2023-02-16/2023-01-16T16:13:21/Polling Stations.csv"
    elections = ["2022-02-16"]
