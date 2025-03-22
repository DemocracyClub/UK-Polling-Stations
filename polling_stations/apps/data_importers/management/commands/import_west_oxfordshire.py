from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOX"
    addresses_name = (
        "2025-05-01/2025-03-18T14:40:33.046028/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-18T14:40:33.046028/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
