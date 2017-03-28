from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000127'
    addresses_name  = 'West Lancashire - PropertyPostCodePollingStationWebLookup-2017-03-08.TSV'
    stations_name   = 'West Lancashire - PropertyPostCodePollingStationWebLookup-2017-03-08.TSV'
    elections       = ['local.lancashire.2017-05-04']
    csv_delimiter = '\t'
