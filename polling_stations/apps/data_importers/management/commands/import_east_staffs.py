from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "EST"
    addresses_name = (
        "2025-05-01/2025-03-20T14:09:10.936427/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2025-05-01/2025-03-20T14:09:10.936427/Democracy Club - Polling Stations.csv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
