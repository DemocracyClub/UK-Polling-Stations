from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TOR"
    addresses_name = (
        "2025-04-17/2025-03-24T16:42:40.256751/Democracy_Club__17April2025.tsv"
    )
    stations_name = (
        "2025-04-17/2025-03-24T16:42:40.256751/Democracy_Club__17April2025Northam.tsv"
    )
    elections = ["2025-04-17"]
    csv_delimiter = "\t"
