from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RIB"
    addresses_name = (
        "2025-05-01/2025-04-09T14:19:45.282804/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-09T14:19:45.282804/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"
