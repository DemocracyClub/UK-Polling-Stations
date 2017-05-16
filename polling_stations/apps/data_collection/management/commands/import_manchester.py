from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000003'
    addresses_name  = 'parl.2017-06-08/Version 1/PropertyPostCodePollingStationWebLookup-2017-05-12.TSV'
    stations_name   = 'parl.2017-06-08/Version 1/PropertyPostCodePollingStationWebLookup-2017-05-12.TSV'
    elections       = [
        'mayor.greater-manchester.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
