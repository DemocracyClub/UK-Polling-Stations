from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000007'
    addresses_name  = 'StockportPropertyPostCodePollingStationWebLookup-2017-02-16.CSV'
    stations_name   = 'StockportPropertyPostCodePollingStationWebLookup-2017-02-16.CSV'
    elections       = [
        'mayor.greater-manchester.2017-05-04',
        'parl.2017-06-08'
    ]
