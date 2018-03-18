from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E08000019'
    addresses_name  = 'local.2018-05-03/Version 1/polling_station_export-2018-03-16.csv'
    stations_name   = 'local.2018-05-03/Version 1/polling_station_export-2018-03-16.csv'
    elections       = ['local.2018-05-03']
    csv_encoding    = 'windows-1252'
