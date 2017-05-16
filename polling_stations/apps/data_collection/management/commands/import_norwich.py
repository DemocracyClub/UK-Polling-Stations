from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000148'
    addresses_name  = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-15.csv'
    stations_name   = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-15.csv'
    elections       = [
        'local.norfolk.2017-05-04',
        'parl.2017-06-08'
    ]
