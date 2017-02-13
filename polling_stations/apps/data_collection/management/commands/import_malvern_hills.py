from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id      = 'E07000235'
    addresses_name  = 'rev02-2017/MalvernHillsPropertyPostCodePollingStationWebLookup-2017-02-03.CSV'
    stations_name   = 'rev02-2017/MalvernHillsPropertyPostCodePollingStationWebLookup-2017-02-03.CSV'
    elections       = ['local.worcestershire.2017-05-04']
