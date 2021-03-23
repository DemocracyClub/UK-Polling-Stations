from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = "2021-03-22T10:19:17.028289/Democracy Club - Polling Districts.csv"
    stations_name = "2021-03-22T10:19:17.028289/Democracy Club - Polling Stations.csv"
    elections = ["2021-05-06"]
    csv_encoding = "latin-1"
