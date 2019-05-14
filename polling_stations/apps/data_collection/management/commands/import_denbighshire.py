from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000004"
    addresses_name = "europarl.2019-05-23/Version 2/Democracy_Club__23May2019den.tsv"
    stations_name = "europarl.2019-05-23/Version 2/Democracy_Club__23May2019den.tsv"
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    elections = ["europarl.2019-05-23"]
