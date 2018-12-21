from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000027"
    addresses_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018 Richmond.CSV"
    stations_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018 Richmond.CSV"
    elections = ["local.2018-05-03"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"
