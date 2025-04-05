from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAR"
    addresses_name = (
        "2025-05-01/2025-04-02T12:50:00.400248/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-04-02T12:50:00.400248/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]
