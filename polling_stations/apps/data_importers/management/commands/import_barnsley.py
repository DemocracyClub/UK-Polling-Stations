from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNS"
    addresses_name = "2023-05-04/2023-04-13T15:16:58.037951/Polling Districts.csv"
    stations_name = "2023-05-04/2023-04-13T15:16:58.037951/Polling Stations.csv"
    elections = ["2023-05-04"]
