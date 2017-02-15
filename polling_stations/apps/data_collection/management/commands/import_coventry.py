from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id      = 'E08000026'
    addresses_name  = 'rev02-2017/CoventryPropertyPostCodePollingStationWebLookup-2017-02-02.TSV'
    stations_name   = 'rev02-2017/CoventryPropertyPostCodePollingStationWebLookup-2017-02-02.TSV'
    elections       = ['mayor.west-midlands.2017-05-04']
    csv_delimiter = '\t'
