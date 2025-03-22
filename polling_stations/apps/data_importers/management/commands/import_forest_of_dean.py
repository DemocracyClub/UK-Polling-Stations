from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FOE"
    addresses_name = (
        "2025-05-01/2025-03-18T10:21:20.040469/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-18T10:21:20.040469/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
