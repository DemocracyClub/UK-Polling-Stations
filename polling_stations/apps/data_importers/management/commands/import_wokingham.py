from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOK"
    addresses_name = (
        "2026-05-07/2025-11-14T16:03:02.301403/Democracy_Club__11December2025.tsv"
    )
    stations_name = (
        "2026-05-07/2025-11-14T16:03:02.301403/Democracy_Club__11December2025.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
