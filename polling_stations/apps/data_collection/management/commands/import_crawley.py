from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id       = 'E07000226'
    addresses_name   = 'May 2017 crawley property and polling station.csv'
    stations_name    = 'May 2017 crawley property and polling station.csv'
    elections        = ['local.west-sussex.2017-05-04']
    station_id_field = 'pollingplace_uprn'
