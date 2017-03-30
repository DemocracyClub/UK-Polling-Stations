from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000005'
    addresses_name  = 'May 2017/RochdalePropertyPostCodePollingStationWebLookup-2017-03-15.TSV'
    stations_name   = 'May 2017/RochdalePropertyPostCodePollingStationWebLookup-2017-03-15.TSV'
    elections       = ['mayor.greater-manchester-ca.2017-05-04']
    csv_delimiter = '\t'
