from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEW"
    addresses_name = (
        "2026-05-07/2026-03-05T12:00:58.887905/Democracy_Club__07May2026 (1).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-05T12:00:58.887905/Democracy_Club__07May2026 (1).tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
