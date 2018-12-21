from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000003"
    addresses_name = "parl.2017-06-08/Version 1/E06000003-Redcar-and-Cleveland Democracy_Club__08June2017.tsv"
    stations_name = "parl.2017-06-08/Version 1/E06000003-Redcar-and-Cleveland Democracy_Club__08June2017.tsv"
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"
