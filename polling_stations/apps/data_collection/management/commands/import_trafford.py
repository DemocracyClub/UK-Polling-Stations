from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000009'
    addresses_name  = 'TraffordPropertyPostCodePollingStationWebLookup-2017-02-10.csv'
    stations_name   = 'TraffordPropertyPostCodePollingStationWebLookup-2017-02-10.csv'
    elections       = [
        'mayor.greater-manchester.2017-05-04',
        'parl.2017-06-08'
    ]
