from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E06000026'
    addresses_name  = 'parl.2017-06-08/Version 1/Plymouth Addresses on database - Polling Stations.csv'
    stations_name   = 'parl.2017-06-08/Version 1/Plymouth Addresses on database - Polling Stations.csv'
    elections       = ['parl.2017-06-08']
    csv_encoding    = 'windows-1252'
