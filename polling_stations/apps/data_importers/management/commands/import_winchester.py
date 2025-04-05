from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = (
        "2025-05-01/2025-03-31T09:13:48.572996/Democracy_Club__01May2025 (7).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-31T09:13:48.572996/Democracy_Club__01May2025 (7).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
