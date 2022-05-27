from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SND"
    addresses_name = (
        "2022-06-16/2022-05-11T09:01:18.723692/Democracy_Club__16June2022.tsv"
    )
    stations_name = (
        "2022-06-16/2022-05-11T09:01:18.723692/Democracy_Club__16June2022.tsv"
    )
    elections = ["2022-06-16"]
    csv_delimiter = "\t"
