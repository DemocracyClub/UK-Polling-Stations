from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000026'
    addresses_name  = 'parl.2017-06-08/Version 1/E08000026-Coventry PropertyPostCodePollingStationWebLookup-2017-05-19.TSV'
    stations_name   = 'parl.2017-06-08/Version 1/E08000026-Coventry PropertyPostCodePollingStationWebLookup-2017-05-19.TSV'
    elections       = ['parl.2017-06-08']
    csv_delimiter = '\t'
