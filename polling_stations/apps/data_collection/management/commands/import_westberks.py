from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000037"
    addresses_name = "parish.west-berkshire.theale.2018-03-15/parish.west-berkshire.theale.2018-03-15.tsv"
    stations_name = "parish.west-berkshire.theale.2018-03-15/parish.west-berkshire.theale.2018-03-15.tsv"
    elections = ["parish.west-berkshire.theale.2018-03-15"]
    csv_delimiter = "\t"
