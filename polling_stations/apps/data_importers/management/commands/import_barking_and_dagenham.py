from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BDG"
    addresses_name = (
        "2026-05-07/2026-03-05T15:43:47.815524/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-05T15:43:47.815524/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
