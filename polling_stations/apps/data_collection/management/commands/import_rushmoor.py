from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000092"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Rushmoor.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Rushmoor.tsv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_delimiter = "\t"
