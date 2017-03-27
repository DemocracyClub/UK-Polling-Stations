from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000123'
    addresses_name  = 'PrestonPropertyPostCodePollingStationWebLookup-2017-02-08.TSV'
    stations_name   = 'PrestonPropertyPostCodePollingStationWebLookup-2017-02-08.TSV'
    elections       = ['local.lancashire.2017-05-04']
    csv_delimiter = '\t'
