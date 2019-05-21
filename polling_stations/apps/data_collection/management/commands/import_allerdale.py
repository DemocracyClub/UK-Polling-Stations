from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000026"
    addresses_name = "europarl.2019-05-23/Version 1/Allerdale Polling Districts for Democracy Club.csv"
    stations_name = "europarl.2019-05-23/Version 1/Allerdale Polling Stations for Democracy Club.csv"
    elections = ["europarl.2019-05-23"]
