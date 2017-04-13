from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'W06000012'
    addresses_name  = 'NPTalbot_polling_station_export-2017-04-13.csv'
    stations_name   = 'NPTalbot_polling_station_export-2017-04-13.csv'
    elections       = ['local.neath-port-talbot.2017-05-04']
    csv_encoding    = 'latin-1'
