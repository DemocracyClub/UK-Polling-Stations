from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000148'
    addresses_name  = 'Norwichpolling_station_export-2017-03-17.csv'
    stations_name   = 'Norwichpolling_station_export-2017-03-17.csv'
    elections       = ['local.norfolk.2017-05-04']
