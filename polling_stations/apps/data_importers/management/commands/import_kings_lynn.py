from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIN"
    addresses_name = (
        "2026-07-16/2026-06-12T15:24:46.009999/Democracy_Club__16July2026.tsv"
    )
    stations_name = (
        "2026-07-16/2026-06-12T15:24:46.009999/Democracy_Club__16July2026.tsv"
    )
    elections = ["2026-07-16"]
    csv_delimiter = "\t"
