from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id = 'E07000004'
    addresses_name = '2017/PropertyPostCodePollingStationWebLookup-2017-05-03.TSV'
    stations_name = '2017/PropertyPostCodePollingStationWebLookup-2017-05-03.TSV'
    elections = ['local.buckinghamshire.2017-05-04']
    csv_delimiter = '\t'
