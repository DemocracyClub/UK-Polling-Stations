from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWL"
    addresses_name = (
        "2025-05-01/2025-03-24T11:11:48.525799/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-24T11:11:48.525799/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]
