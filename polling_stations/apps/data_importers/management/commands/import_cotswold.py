from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COT"
    addresses_name = (
        "2025-05-01/2025-03-10T12:04:49.155852/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-10T12:04:49.155852/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
