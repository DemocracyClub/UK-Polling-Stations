from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000090'
    addresses_name  = 'HavantPropertyPostCodePollingStationWebLookup-2017-03-20.TSV'
    stations_name   = 'HavantPropertyPostCodePollingStationWebLookup-2017-03-20.TSV'
    elections       = [
        'local.hampshire.2017-05-04',
        #'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
