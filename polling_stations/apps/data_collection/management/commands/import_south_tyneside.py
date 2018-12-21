from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000023"
    addresses_name = (
        "local.2018-05-03/Version 2/Democracy_Club__03May2018 - South Tyneside.tsv"
    )
    stations_name = (
        "local.2018-05-03/Version 2/Democracy_Club__03May2018 - South Tyneside.tsv"
    )
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
