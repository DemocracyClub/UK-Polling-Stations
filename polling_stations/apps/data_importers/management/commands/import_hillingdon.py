from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIL"
    addresses_name = "2023-07-20/2023-06-26T14:07:37/Democracy_Club__20July2023_HIL.tsv"
    stations_name = "2023-07-20/2023-06-26T14:07:37/Democracy_Club__20July2023_HIL.tsv"
    elections = ["2023-07-20"]
    csv_delimiter = "\t"
