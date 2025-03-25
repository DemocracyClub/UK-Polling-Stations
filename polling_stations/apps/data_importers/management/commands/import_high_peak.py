from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIG"
    addresses_name = (
        "2025-05-01/2025-03-25T10:11:00.608557/Democracy_Club__01May2025 (5).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-25T10:11:00.608557/Democracy_Club__01May2025 (5).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
