from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LBH"
    addresses_name = (
        "2023-10-05/2023-09-29T10:50:35.830333/Democracy_Club__05October2023.tsv"
    )
    stations_name = (
        "2023-10-05/2023-09-29T10:50:35.830333/Democracy_Club__05October2023.tsv"
    )
    elections = ["2023-10-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
