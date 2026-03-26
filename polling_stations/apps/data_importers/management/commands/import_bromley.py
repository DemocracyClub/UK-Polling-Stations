from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRY"
    addresses_name = (
        "2026-05-07/2026-03-26T12:21:15.298569/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-26T12:21:15.298569/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
