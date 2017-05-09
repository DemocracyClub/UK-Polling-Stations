from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000010'
    addresses_name  = 'WiganNewPropertyPollingStation_master.csv'
    stations_name   = 'WiganNewPropertyPollingStation_master.csv'
    elections       = [
        'mayor.greater-manchester-ca.2017-05-04',
        'parl.2017-06-08'
    ]
