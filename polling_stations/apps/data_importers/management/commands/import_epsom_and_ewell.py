from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EPS"
    addresses_name = (
        "2026-05-07/2026-03-26T08:58:28.457886/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-26T08:58:28.457886/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
