from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOK"
    addresses_name = (
        "2026-05-07/2026-01-07T09:59:24.987151/Democracy_Club__11December2025.tsv"
    )
    stations_name = (
        "2026-05-07/2026-01-07T09:59:24.987151/Democracy_Club__11December2025.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
