from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000118'
    addresses_name  = 'May 2017/Chorley_polling_station_export-2017-03-03.csv'
    stations_name   = 'May 2017/Chorley_polling_station_export-2017-03-03.csv'
    elections       = [
        'local.lancashire.2017-05-04',
        'parl.2017-06-08'
    ]
