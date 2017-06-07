from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id = 'E09000032'
    addresses_name = 'parl.2017-06-08/Version 2/PropertyPostCodePollingStationWebLookup-2017-05-03 (1).TSV'
    stations_name = 'parl.2017-06-08/Version 2/PropertyPostCodePollingStationWebLookup-2017-05-03 (1).TSV'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
