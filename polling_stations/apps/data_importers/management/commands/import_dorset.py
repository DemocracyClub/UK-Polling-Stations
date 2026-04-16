from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DST"
    addresses_name = (
        "2026-05-21/2026-04-16T14:31:44.250946/Democracy_Club__21May2026.tsv"
    )
    stations_name = (
        "2026-05-21/2026-04-16T14:31:44.250946/Democracy_Club__21May2026.tsv"
    )
    elections = ["2026-05-21"]
    csv_delimiter = "\t"
