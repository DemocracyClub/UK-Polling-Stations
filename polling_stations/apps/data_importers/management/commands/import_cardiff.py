from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = (
        "2026-05-07/2025-11-21T10:59:47.830995/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2026-05-07/2025-11-21T10:59:47.830995/Democracy_Club__02May2024.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
