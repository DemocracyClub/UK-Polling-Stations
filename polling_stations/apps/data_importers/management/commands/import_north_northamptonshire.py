from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNT"
    addresses_name = (
        "2024-02-15/2024-01-29T15:50:58.118774/Democracy_Club__15February2024.tsv"
    )
    stations_name = (
        "2024-02-15/2024-01-29T15:50:58.118774/Democracy_Club__15February2024.tsv"
    )
    elections = ["2024-02-15"]
    csv_delimiter = "\t"
