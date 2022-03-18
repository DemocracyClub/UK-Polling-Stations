from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = (
        "2022-05-05/2022-03-18T16:35:41.044948/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-18T16:35:41.044948/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"
