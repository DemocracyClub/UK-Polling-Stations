from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RED"
    addresses_name = (
        "2025-05-01/2025-03-05T12:04:07.695909/Democracy_Club__01May2025 Redditch.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-05T12:04:07.695909/Democracy_Club__01May2025 Redditch.CSV"
    )
    elections = ["2025-05-01"]
