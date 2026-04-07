from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IOW"
    addresses_name = (
        "2026-05-07/2026-04-07T16:00:02.432211/Democracy_Club__07May2026_fixed.CSV"
    )
    stations_name = (
        "2026-05-07/2026-04-07T16:00:02.432211/Democracy_Club__07May2026_fixed.CSV"
    )
    elections = ["2026-05-07"]
