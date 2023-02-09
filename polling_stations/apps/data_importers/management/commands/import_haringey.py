from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRY"
    addresses_name = (
        "2023-03-09/2023-02-09T10:24:24.779394/Democracy_Club__09March2023.tsv"
    )
    stations_name = (
        "2023-03-09/2023-02-09T10:24:24.779394/Democracy_Club__09March2023.tsv"
    )
    elections = ["2023-03-09"]
    csv_delimiter = "\t"
