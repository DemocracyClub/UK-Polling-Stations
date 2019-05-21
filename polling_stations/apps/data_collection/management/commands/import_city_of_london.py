from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000001"
    addresses_name = "europarl.2019-05-23/Version 1/Data for Democracy Club.csv"
    stations_name = "europarl.2019-05-23/Version 1/Data for Democracy Club.csv"
    elections = ["europarl.2019-05-23"]
