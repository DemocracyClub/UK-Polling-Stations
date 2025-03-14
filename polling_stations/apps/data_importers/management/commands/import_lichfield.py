from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIF"
    addresses_name = (
        "2025-05-01/2025-03-11T14:11:49.793927/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-11T14:11:49.793927/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
