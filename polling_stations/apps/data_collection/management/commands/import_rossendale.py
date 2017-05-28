from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id = 'E07000125'
    addresses_name = 'parl.2017-06-08/Version 2/Rossendale and Darwen PropertyPostCodePollingStationWebLookup-2017-05-24.TSV'
    stations_name = 'parl.2017-06-08/Version 2/Rossendale and Darwen PropertyPostCodePollingStationWebLookup-2017-05-24.TSV'
    elections = ['parl.2017-06-08']
