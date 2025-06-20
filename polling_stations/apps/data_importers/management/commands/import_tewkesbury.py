from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEW"
    addresses_name = (
        "2025-07-10/2025-06-20T10:37:50.424790/Democracy_Club__10July2025.tsv"
    )
    stations_name = (
        "2025-07-10/2025-06-20T10:37:50.424790/Democracy_Club__10July2025.tsv"
    )
    elections = ["2025-07-10"]
    csv_delimiter = "\t"
