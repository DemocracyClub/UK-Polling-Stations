from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYR"
    addresses_name = (
        "2025-05-01/2025-03-11T12:33:48.183418/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-11T12:33:48.183418/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
