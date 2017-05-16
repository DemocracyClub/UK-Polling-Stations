from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E06000050'
    addresses_name  = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-12.csv'
    stations_name   = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-12.csv'
    elections       = ['parl.2017-06-08']
    csv_encoding    = 'windows-1252'
