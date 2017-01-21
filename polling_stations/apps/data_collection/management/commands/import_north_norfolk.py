from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id      = 'E07000147'
    addresses_name  = 'PropertyPostCodePollingStationWebLookup-2017-01-16.CSV'
    stations_name   = 'PropertyPostCodePollingStationWebLookup-2017-01-16.CSV'
    elections       = ['local.norfolk.2017-05-04']
