from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = (
        "2022-11-10/2022-10-17T16:55:49.332386/Democracy_Club__10November2022.tsv"
    )
    stations_name = (
        "2022-11-10/2022-10-17T16:55:49.332386/Democracy_Club__10November2022.tsv"
    )
    elections = ["2022-11-10"]
    csv_delimiter = "\t"
