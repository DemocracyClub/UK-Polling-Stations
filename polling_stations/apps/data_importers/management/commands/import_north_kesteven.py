from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2024-03-21/2024-03-01T10:05:32.666182/Democracy_Club__21March2024 (1).tsv"
    )
    stations_name = (
        "2024-03-21/2024-03-01T10:05:32.666182/Democracy_Club__21March2024 (1).tsv"
    )
    elections = ["2024-03-21"]
    csv_delimiter = "\t"
