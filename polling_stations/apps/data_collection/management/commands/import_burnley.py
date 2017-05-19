from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000117'
    # note: extension is TSV, but file is actually comma seperated
    addresses_name  = 'BurnleyPropertyPostCodePollingStationWebLookup-2017-03-10.TSV'
    stations_name   = 'BurnleyPropertyPostCodePollingStationWebLookup-2017-03-10.TSV'
    elections       = [
        'local.lancashire.2017-05-04',
        #'parl.2017-06-08'
    ]
