from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GLO"
    addresses_name = (
        "2025-05-01/2025-03-25T16:38:03.119595/Democracy_Club__01May2025_GLOUCESTER.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-25T16:38:03.119595/Democracy_Club__01May2025_GLOUCESTER.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
