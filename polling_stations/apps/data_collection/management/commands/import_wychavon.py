from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id      = 'E07000238'
    addresses_name  = 'WychavonPropertyPostCodePollingStationWebLookup-2017-02-13.TSV'
    stations_name   = 'WychavonPropertyPostCodePollingStationWebLookup-2017-02-13.TSV'
    elections       = ['local.worcestershire.2017-05-04']
    csv_delimiter = '\t'
