from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000109'
    addresses_name  = 'May 2017 - new data/Gravesham2polling_station_export-2017-04-06.csv'
    stations_name   = 'May 2017 - new data/Gravesham2polling_station_export-2017-04-06.csv'
    elections       = ['local.kent.2017-05-04']
    csv_encoding    = 'latin-1'
