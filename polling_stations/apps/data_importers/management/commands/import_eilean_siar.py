from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ELS"
    addresses_name = "2024-07-04/2024-06-06T13:12:09.503968/Democracy Club - Polling Districts NHEAI.csv"
    stations_name = "2024-07-04/2024-06-06T13:12:09.503968/Democracy Club - Polling Stations NHEAI.csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"
