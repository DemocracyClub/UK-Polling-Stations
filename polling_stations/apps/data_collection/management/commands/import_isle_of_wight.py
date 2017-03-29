from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E06000046'
    addresses_name  = 'rev02-2017/IsleofWightPropertyPostCodePollingStationWebLookup-2017-02-07.TSV'
    stations_name   = 'rev02-2017/IsleofWightPropertyPostCodePollingStationWebLookup-2017-02-07.TSV'
    elections       = ['local.isle-of-wight.2017-05-04']
    csv_delimiter = '\t'
