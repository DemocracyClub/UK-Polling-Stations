from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id = 'E07000228'
    addresses_name = 'MidSussexDemocracy Club Data-2017-04-10.TSV'
    stations_name = 'MidSussexDemocracy Club Data-2017-04-10.TSV'
    elections = [
        'local.west-sussex.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
