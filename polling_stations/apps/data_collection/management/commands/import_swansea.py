from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'W06000011'
    addresses_name  = 'May 2017/Swansea_polling_station_export-2017-03-06.csv'
    stations_name   = 'May 2017/Swansea_polling_station_export-2017-03-06.csv'
    elections       = ['local.swansea.2017-05-04']
    csv_encoding    = 'latin-1'
