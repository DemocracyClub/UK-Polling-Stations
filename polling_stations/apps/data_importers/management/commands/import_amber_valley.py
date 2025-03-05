from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "AMB"
    addresses_name = (
        "2025-05-01/2025-03-05T12:10:33.836869/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2025-05-01/2025-03-05T12:10:33.836869/Democracy Club - Polling Stations.csv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
