from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FLN"
    addresses_name = "2026-05-07/2026-02-27T11:02:16.435939/Democracy_Club__07May2026 - Flintshire.CSV"
    stations_name = "2026-05-07/2026-02-27T11:02:16.435939/Democracy_Club__07May2026 - Flintshire.CSV"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
