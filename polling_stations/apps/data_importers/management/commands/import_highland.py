from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = "2024-06-13/2024-05-20T10:40:21.769643/Democracy Club - Polling Districts W7.csv"
    stations_name = (
        "2024-06-13/2024-05-20T10:40:21.769643/Democracy Club - Polling Stations W7.csv"
    )
    elections = ["2024-06-13"]
    csv_encoding = "utf-16le"
