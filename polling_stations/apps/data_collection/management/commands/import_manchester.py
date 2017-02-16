from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id      = 'E08000003'
    addresses_name  = 'ManchesterPropertyPostCodePollingStationWebLookup-2017-02-16.TSV'
    stations_name   = 'ManchesterPropertyPostCodePollingStationWebLookup-2017-02-16.TSV'
    elections       = ['mayor.greater-manchester.2017-05-04']
    csv_delimiter = '\t'
