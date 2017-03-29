from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000125'
    # note: extension is TSV, but file is actually comma seperated
    addresses_name  = 'RossendalePropertyPostCodePollingStationWebLookup-2017-03-10.TSV'
    stations_name   = 'RossendalePropertyPostCodePollingStationWebLookup-2017-03-10.TSV'
    elections       = ['local.lancashire.2017-05-04']
