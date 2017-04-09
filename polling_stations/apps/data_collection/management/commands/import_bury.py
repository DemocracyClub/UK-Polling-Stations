from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000002'
    addresses_name  = 'PropertyPostCodePollingStationWebLookup-2017-03-08.CSV'
    stations_name   = 'PropertyPostCodePollingStationWebLookup-2017-03-08.CSV'
    elections       = ['mayor.greater-manchester-ca.2017-05-04']
