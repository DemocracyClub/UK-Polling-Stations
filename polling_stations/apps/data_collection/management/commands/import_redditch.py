from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000236'
    addresses_name  = 'RBC Polling Station look up data.csv'
    stations_name   = 'RBC Polling Station look up data.csv'
    elections       = ['local.worcestershire.2017-05-04']
