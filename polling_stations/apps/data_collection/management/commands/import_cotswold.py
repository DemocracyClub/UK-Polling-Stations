from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id = 'E07000079'
    addresses_name = 'CotswoldsPropertyPostCodePollingStationWebLookup-2017-02-28.TSV'
    stations_name = 'CotswoldsPropertyPostCodePollingStationWebLookup-2017-02-28.TSV'
    elections = ['local.gloucestershire.2017-05-04']
    csv_delimiter = '\t'
