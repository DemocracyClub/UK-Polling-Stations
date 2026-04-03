from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WEA"
    addresses_name = (
        "2026-05-07/2026-03-27T16:12:54.336801/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-27T16:12:54.336801/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
