from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BBD"
    addresses_name = (
        "2026-05-07/2026-03-24T11:41:56.121266/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-24T11:41:56.121266/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
