from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNT"
    addresses_name = (
        "2024-02-15/2024-01-25T10:56:24.479815/Democracy_Club__15February2024.tsv"
    )
    stations_name = (
        "2024-02-15/2024-01-25T10:56:24.479815/Democracy_Club__15February2024.tsv"
    )
    elections = ["2024-02-15"]
    csv_delimiter = "\t"
