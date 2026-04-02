from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOL"
    addresses_name = (
        "2026-05-07/2026-04-02T15:14:58.840898/Democracy_Club__07May2026_Bolton.CSV"
    )
    stations_name = (
        "2026-05-07/2026-04-02T15:14:58.840898/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
