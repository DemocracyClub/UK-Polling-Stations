from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000102"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.CSV"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.CSV"
    elections = ["local.2018-05-03"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"
