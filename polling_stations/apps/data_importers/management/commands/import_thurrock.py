from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THR"
    addresses_name = (
        "2025-05-01/2025-03-26T14:00:22.033216/Democracy_Club__01May2025 (6).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-26T14:00:22.033216/Democracy_Club__01May2025 (6).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
