from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000008'
    addresses_name  = 'TamesidePropertyPostCodePollingStationWebLookup-2017-03-15.TSV'
    stations_name   = 'TamesidePropertyPostCodePollingStationWebLookup-2017-03-15.TSV'
    elections       = [
        'mayor.greater-manchester-ca.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
