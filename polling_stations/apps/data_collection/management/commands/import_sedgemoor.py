from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000188'
    addresses_name  = 'Sedgemoor_polling_station_export-2017-02-24.csv'
    stations_name   = 'Sedgemoor_polling_station_export-2017-02-24.csv'
    elections       = [
        'local.somerset.2017-05-04',
        'parl.2017-06-08'
    ]
