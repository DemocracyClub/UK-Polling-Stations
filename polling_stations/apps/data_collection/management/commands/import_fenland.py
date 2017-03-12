from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000010'
    addresses_name  = 'Fenland_polling_station_export-2017-03-06.csv'
    stations_name   = 'Fenland_polling_station_export-2017-03-06.csv'
    elections       = ['mayor.cambridgeshire-and-peterborough.2017-05-04']
