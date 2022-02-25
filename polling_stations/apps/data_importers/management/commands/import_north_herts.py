from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NHE"
    addresses_name = (
        "2022-03-10/2022-02-25T09:45:13.978912/Democracy_Club__10March2022.tsv"
    )
    stations_name = (
        "2022-03-10/2022-02-25T09:45:13.978912/Democracy_Club__10March2022.tsv"
    )
    elections = ["2022-03-10"]
    csv_delimiter = "\t"
