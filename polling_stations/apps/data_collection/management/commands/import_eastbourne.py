from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000061'
    addresses_name  = 'Eastbourne_polling_station_export-2017-02-24.csv'
    stations_name   = 'Eastbourne_polling_station_export-2017-02-24.csv'
    elections       = [
        'local.east-sussex.2017-05-04',
        'parl.2017-06-08'
    ]
