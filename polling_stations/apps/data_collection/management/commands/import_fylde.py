from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000119'
    addresses_name  = 'Fylde Democracy Club.CSV'
    stations_name   = 'Fylde Democracy Club.CSV'
    elections       = ['local.lancashire.2017-05-04']
