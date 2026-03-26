from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KEC"
    addresses_name = (
        "2026-05-07/2026-03-23T15:39:45.538368/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-23T15:39:45.538368/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
