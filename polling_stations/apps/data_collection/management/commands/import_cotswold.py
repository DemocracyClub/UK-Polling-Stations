from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id = 'E07000079'
    addresses_name = 'parl.2017-06-08/Version 1/PropertyPostCodePollingStationWebLookup-2017-06-02.TSV'
    stations_name = 'parl.2017-06-08/Version 1/PropertyPostCodePollingStationWebLookup-2017-06-02.TSV'
    elections = ['parl.2017-06-08']
