from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000004'
    addresses_name  = '21 Mar new version/Oldham2PropertyPostCodePollingStationWebLookup-2017-03-20.TSV'
    stations_name   = '21 Mar new version/Oldham2PropertyPostCodePollingStationWebLookup-2017-03-20.TSV'
    elections       = ['mayor.greater-manchester.2017-05-04']
    csv_delimiter = '\t'
