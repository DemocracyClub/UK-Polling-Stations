from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E08000030'
    addresses_name  = 'polling_station_export-2017-05-02.csv'
    stations_name   = 'polling_station_export-2017-05-02.csv'
    elections       = ['mayor.west-midlands.2017-05-04']
    csv_encoding    = 'latin-1'
