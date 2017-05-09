from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000120'
    addresses_name  = 'rev02-2017/Hyndburn_polling_station_export-2017-02-03 (1).csv'
    stations_name   = 'rev02-2017/Hyndburn_polling_station_export-2017-02-03 (1).csv'
    elections       = [
        'local.lancashire.2017-05-04',
        'parl.2017-06-08'
    ]
