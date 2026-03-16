from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THR"
    addresses_name = (
        "2026-05-07/2026-03-16T14:11:49.479694/Democracy_Club__07May2026 (3).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-16T14:11:49.479694/Democracy_Club__07May2026 (3).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
