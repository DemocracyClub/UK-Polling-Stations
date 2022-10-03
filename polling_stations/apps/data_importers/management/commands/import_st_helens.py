from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2022-10-20/2022-10-03T17:06:44.959671/Democracy_Club__20October2022.tsv"
    )
    stations_name = (
        "2022-10-20/2022-10-03T17:06:44.959671/Democracy_Club__20October2022.tsv"
    )
    elections = ["2022-10-20"]
    csv_delimiter = "\t"
