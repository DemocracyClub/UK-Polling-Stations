from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIL"
    addresses_name = (
        "2025-10-09/2025-09-18T14:22:55.468140/Democracy_Club__09October2025.tsv"
    )
    stations_name = (
        "2025-10-09/2025-09-18T14:22:55.468140/Democracy_Club__09October2025.tsv"
    )
    elections = ["2025-10-09"]
    csv_delimiter = "\t"
