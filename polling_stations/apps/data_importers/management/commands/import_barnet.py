from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = (
        "2025-10-30/2025-10-13T10:15:59.127701/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2025-10-30/2025-10-13T10:15:59.127701/Democracy Club - Polling Stations.csv"
    )
    elections = ["2025-10-30"]
    csv_encoding = "utf-16le"
