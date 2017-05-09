from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E09000029'
    addresses_name  = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-08.csv'
    stations_name   = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-08.csv'
    elections       = ['parl.2017-06-08']
    csv_encoding    = 'latin-1'
