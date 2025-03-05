from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRM"
    addresses_name = (
        "2025-05-01/2025-03-05T12:03:17.688205/Democracy_Club__01May2025 Bromsgrove.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-05T12:03:17.688205/Democracy_Club__01May2025 Bromsgrove.CSV"
    )
    elections = ["2025-05-01"]
