from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLL"
    addresses_name = (
        "2025-09-11/2025-08-07T15:55:12.153915/Democracy_Club__11September2025.tsv"
    )
    stations_name = (
        "2025-09-11/2025-08-07T15:55:12.153915/Democracy_Club__11September2025.tsv"
    )
    elections = ["2025-09-11"]
    csv_delimiter = "\t"
