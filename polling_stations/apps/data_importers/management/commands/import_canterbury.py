from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAT"
    addresses_name = (
        "2025-05-01/2025-03-13T14:43:22.853120/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-13T14:43:22.853120/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]
