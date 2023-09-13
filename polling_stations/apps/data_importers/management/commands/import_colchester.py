from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2023-09-21/2023-09-13T16:58:37.636307/Democracy_Club__21September2023.tsv"
    )
    stations_name = (
        "2023-09-21/2023-09-13T16:58:37.636307/Democracy_Club__21September2023.tsv"
    )
    elections = ["2023-09-21"]
    csv_delimiter = "\t"
