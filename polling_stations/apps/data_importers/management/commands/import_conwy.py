from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CWY"
    addresses_name = (
        "2026-05-07/2026-02-20T10:35:01.417013/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-02-20T10:35:01.417013/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
