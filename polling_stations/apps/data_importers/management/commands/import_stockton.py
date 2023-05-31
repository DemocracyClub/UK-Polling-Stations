from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STT"
    addresses_name = (
        "2023-06-22/2023-05-31T14:44:53.803777/Democracy_Club__22June2023.tsv"
    )
    stations_name = (
        "2023-06-22/2023-05-31T14:44:53.803777/Democracy_Club__22June2023.tsv"
    )
    elections = ["2023-06-22"]
    csv_delimiter = "\t"
