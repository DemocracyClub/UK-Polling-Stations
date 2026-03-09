from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HPL"
    addresses_name = (
        "2026-05-07/2026-03-09T16:31:17.161293/Democracy_Club__07May2026 (2).CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-09T16:31:17.161293/Democracy_Club__07May2026 (2).CSV"
    )
    elections = ["2026-05-07"]
