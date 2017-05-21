from data_collection.management.commands import BaseDemocracyCountsCsvImporter

class Command(BaseDemocracyCountsCsvImporter):
    council_id = 'E09000003'
    addresses_name = 'parl.2017-06-08/Version 2/Democracy Club - Polling Districts.csv'
    stations_name = 'parl.2017-06-08/Version 2/Democracy Club - Polling Stations.csv'
    elections = ['parl.2017-06-08']
