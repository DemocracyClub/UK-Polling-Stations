from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id       = 'E07000234'
    addresses_name   = 'May 2017/BromsgrovePropertyPostCodePollingStationWebLookup-2017-03-22 2.TSV'
    stations_name    = 'May 2017/BromsgrovePropertyPostCodePollingStationWebLookup-2017-03-22 2.TSV'
    elections        = [
        'local.worcestershire.2017-05-04',
        'parl.2017-06-08'
    ]
