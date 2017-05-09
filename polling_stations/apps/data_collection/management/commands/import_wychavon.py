from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000238'
    addresses_name  = 'WychavonPropertyPostCodePollingStationWebLookup-2017-02-13.TSV'
    stations_name   = 'WychavonPropertyPostCodePollingStationWebLookup-2017-02-13.TSV'
    elections       = [
        'local.worcestershire.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
