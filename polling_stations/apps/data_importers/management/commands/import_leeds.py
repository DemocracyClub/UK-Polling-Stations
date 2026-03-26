from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LDS"
    addresses_name = "2026-05-07/2026-03-23T13:53:24.869634/Democracy_Club__07May2026 amended version.tsv"
    stations_name = "2026-05-07/2026-03-23T13:53:24.869634/Democracy_Club__07May2026 amended version.tsv"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
