from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = (
        "2025-03-06/2025-02-10T12:43:03.278468/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2025-03-06/2025-02-10T12:43:03.278468/Democracy Club - Polling Stations.csv"
    )
    elections = ["2025-03-06"]
    csv_encoding = "utf-16le"
