from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAS"
    addresses_name = (
        "2025-05-01/2025-03-10T10:23:31.659610/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-10T10:23:31.659610/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]
