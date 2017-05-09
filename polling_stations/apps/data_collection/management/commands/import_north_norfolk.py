from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000147'
    addresses_name  = 'PropertyPostCodePollingStationWebLookup-2017-01-16.CSV'
    stations_name   = 'PropertyPostCodePollingStationWebLookup-2017-01-16.CSV'
    elections       = [
        'local.norfolk.2017-05-04',
        'parl.2017-06-08'
    ]
