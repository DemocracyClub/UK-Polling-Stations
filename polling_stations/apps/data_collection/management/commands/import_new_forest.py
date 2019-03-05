from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000091"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019newforest.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019newforest.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
