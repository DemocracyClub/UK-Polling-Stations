from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUN"
    addresses_name = (
        "2026-05-07/2026-03-17T08:09:31.347670/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-17T08:09:31.347670/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
