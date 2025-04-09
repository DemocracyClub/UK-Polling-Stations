from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IOW"
    addresses_name = (
        "2025-05-01/2025-04-09T09:59:02.710426/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-09T09:59:02.710426/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
