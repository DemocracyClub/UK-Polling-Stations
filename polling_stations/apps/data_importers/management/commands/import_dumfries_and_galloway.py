from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DGY"
    addresses_name = "2024-06-27/2024-06-06T10:38:14.688830/Democracy Club - Dumfries and Galloway Polling Districts.csv"
    stations_name = "2024-06-27/2024-06-06T10:38:14.688830/Democracy Club - Dumfries and Galloway Polling Stations.csv"
    elections = ["2024-06-27"]
    csv_encoding = "utf-16le"
