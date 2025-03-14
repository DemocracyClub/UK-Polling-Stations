from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SCA"
    addresses_name = (
        "2025-05-01/2025-03-14T09:31:36.010664/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-14T09:31:36.010664/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
