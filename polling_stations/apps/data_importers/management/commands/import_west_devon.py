from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WDE"
    addresses_name = (
        "2025-05-01/2025-03-19T17:07:01.840411/Democracy_Club__01May2025 (3).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-19T17:07:01.840411/Democracy_Club__01May2025 (3).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
