from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PRE"
    addresses_name = (
        "2026-05-07/2026-03-18T17:08:38.362206/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-18T17:08:38.362206/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
