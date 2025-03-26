from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CON"
    addresses_name = (
        "2025-05-01/2025-03-26T14:41:05.807414/Democracy_Club__01May2025 1.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-26T14:41:05.807414/Democracy_Club__01May2025 1.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
