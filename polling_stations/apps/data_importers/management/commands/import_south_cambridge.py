from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SCA"
    addresses_name = (
        "2022-11-03/2022-10-06T09:58:47.244148/Democracy_Club__03November2022.tsv"
    )
    stations_name = (
        "2022-11-03/2022-10-06T09:58:47.244148/Democracy_Club__03November2022.tsv"
    )
    elections = ["2022-11-03"]
    csv_delimiter = "\t"
