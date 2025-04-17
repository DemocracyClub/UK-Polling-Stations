from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIG"
    addresses_name = (
        "2025-05-01/2025-04-03T15:02:58.158470/Democracy_Club__01May2025 (10).tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-03T15:02:58.158470/Democracy_Club__01May2025 (10).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
