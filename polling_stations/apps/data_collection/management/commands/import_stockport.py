from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000007'
    addresses_name  = 'parl.2017-06-08/Version 1/PropertyPostCodePollingStationWebLookup-2017-05-18.CSV'
    stations_name   = 'parl.2017-06-08/Version 1/PropertyPostCodePollingStationWebLookup-2017-05-18.CSV'
    elections       = ['parl.2017-06-08']
