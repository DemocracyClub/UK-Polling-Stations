from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = (
        "2025-02-13/2025-01-16T10:13:41.822386/Polling District data Burnt Oak.csv"
    )
    stations_name = (
        "2025-02-13/2025-01-16T10:13:41.822386/Polling Station data Burnt Oak.csv"
    )
    elections = ["2025-02-13"]
    csv_encoding = "utf-16le"
