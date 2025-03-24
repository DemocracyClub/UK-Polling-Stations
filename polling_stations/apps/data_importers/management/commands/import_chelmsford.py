from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = (
        "2025-05-01/2025-03-24T15:58:38.061989/Democracy_Club__01May2025 (4).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-24T15:58:38.061989/Democracy_Club__01May2025 (4).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
