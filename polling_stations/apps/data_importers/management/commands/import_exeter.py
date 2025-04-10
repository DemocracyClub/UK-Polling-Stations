from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = (
        "2025-05-01/2025-04-10T12:52:21.787573/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-04-10T12:52:21.787573/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]
