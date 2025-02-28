from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDE"
    addresses_name = (
        "2025-05-01/2025-02-28T12:05:41.703963/Democracy_Club__01May2025 MID DEVON.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-28T12:05:41.703963/Democracy_Club__01May2025 MID DEVON.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
