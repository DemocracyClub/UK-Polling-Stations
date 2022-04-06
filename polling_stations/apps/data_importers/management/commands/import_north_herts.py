from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NHE"
    addresses_name = (
        "2022-05-05/2022-04-06T11:54:12.737798/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-06T11:54:12.737798/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"
