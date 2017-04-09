from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000003'
    addresses_name  = 'ManchesterPropertyPostCodePollingStationWebLookup-2017-04-06.TSV'
    stations_name   = 'ManchesterPropertyPostCodePollingStationWebLookup-2017-04-06.TSV'
    elections       = ['mayor.greater-manchester.2017-05-04']
    csv_delimiter = '\t'
