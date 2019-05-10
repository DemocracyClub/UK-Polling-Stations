from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000036"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019BF.tsv"

    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019BF.tsv"

    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
