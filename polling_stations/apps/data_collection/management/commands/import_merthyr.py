from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'W06000024'
    addresses_name  = 'Merthyr_polling_station_export-2017-04-13.csv'
    stations_name   = 'Merthyr_polling_station_export-2017-04-13.csv'
    elections       = [
        'local.merthyr-tydfil.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_encoding    = 'latin-1'
