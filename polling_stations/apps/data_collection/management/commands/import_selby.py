from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000169"
    addresses_name = "SelbyDemocracy_Club__04May2017.tsv"
    stations_name = "SelbyDemocracy_Club__04May2017.tsv"
    elections = ["local.north-yorkshire.2017-05-04", "parl.2017-06-08"]
    csv_delimiter = "\t"
