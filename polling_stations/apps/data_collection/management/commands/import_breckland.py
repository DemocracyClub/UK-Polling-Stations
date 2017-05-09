from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000143'
    addresses_name  = 'May 2017/BrecklandPropertyPostCodePollingStationWebLookup-2017-02-20.TSV'
    stations_name   = 'May 2017/BrecklandPropertyPostCodePollingStationWebLookup-2017-02-20.TSV'
    elections       = [
        'local.norfolk.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
