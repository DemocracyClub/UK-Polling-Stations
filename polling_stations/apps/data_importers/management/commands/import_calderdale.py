from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CLD"
    addresses_name = "2026-05-07/2026-03-17T16:40:35.655763/20260317_Democracy_Club__07May2026_CMBC.CSV"
    stations_name = "2026-05-07/2026-03-17T16:40:35.655763/20260317_Democracy_Club__07May2026_CMBC.CSV"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
