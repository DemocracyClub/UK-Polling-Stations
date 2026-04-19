from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAS"
    addresses_name = (
        "2026-05-07/2026-04-19T14:20:06.301370/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-19T14:20:06.301370/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
