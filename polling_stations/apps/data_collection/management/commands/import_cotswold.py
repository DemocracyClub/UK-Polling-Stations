from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id = 'E07000079'
    addresses_name = 'CotswoldPropertyPostCodePollingStationWebLookup-2017-03-27.TSV'
    stations_name = 'CotswoldPropertyPostCodePollingStationWebLookup-2017-03-27.TSV'
    elections = ['local.gloucestershire.2017-05-04']
    csv_delimiter = '\t'
