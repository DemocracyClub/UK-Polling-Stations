from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IOW"
    addresses_name = (
        "2026-05-07/2026-03-27T11:29:48.036646/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-27T11:29:48.036646/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
