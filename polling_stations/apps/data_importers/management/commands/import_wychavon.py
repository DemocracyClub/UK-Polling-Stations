from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYC"
    addresses_name = (
        "2025-05-01/2025-03-05T16:28:55.760571/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-05T16:28:55.760571/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
