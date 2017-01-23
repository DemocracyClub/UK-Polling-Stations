from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id = 'E07000004'
    addresses_name = 'Aylesbury Vale PropertyPostCodePollingStationWebLookup-2016-11-21-fixed.CSV'
    stations_name = 'Aylesbury Vale PropertyPostCodePollingStationWebLookup-2016-11-21-fixed.CSV'
    elections = ['local.buckinghamshire.2017-05-04']
