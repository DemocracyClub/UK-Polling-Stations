from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id = 'E07000122'
    addresses_name = 'PendlePropertyPostCodePollingStationWebLookup-2017-03-01.TSV'
    stations_name = 'PendlePropertyPostCodePollingStationWebLookup-2017-03-01.TSV'
    elections = [
        'local.lancashire.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
