from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "AMB"
    addresses_name = "2021-03-16T14:36:13.602969/Democracy Club - Polling Districts.csv"
    stations_name = "2021-03-16T14:36:13.602969/Democracy Club - Polling Stations.csv"
    elections = ["2021-05-06"]
