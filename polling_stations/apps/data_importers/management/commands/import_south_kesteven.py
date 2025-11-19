from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = (
        "2025-12-11/2025-11-19T16:20:29.085210/Democracy_Club__11December2025.tsv"
    )
    stations_name = (
        "2025-12-11/2025-11-19T16:20:29.085210/Democracy_Club__11December2025.tsv"
    )
    elections = ["2025-12-11"]
    csv_delimiter = "\t"
