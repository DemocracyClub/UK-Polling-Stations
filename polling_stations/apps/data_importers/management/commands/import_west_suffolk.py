from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WSK"
    addresses_name = (
        "2026-05-07/2026-03-17T15:32:06.667126/Democracy_Club__07May2026 (1).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T15:32:06.667126/Democracy_Club__07May2026 (1).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
