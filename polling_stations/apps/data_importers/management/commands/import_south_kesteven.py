from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = (
        "2025-05-01/2025-02-28T11:55:34.407771/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-28T11:55:34.407771/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
