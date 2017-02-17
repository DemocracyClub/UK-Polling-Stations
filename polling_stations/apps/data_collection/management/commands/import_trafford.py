from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id      = 'E08000009'
    addresses_name  = 'TraffordPropertyPostCodePollingStationWebLookup-2017-02-10.csv'
    stations_name   = 'TraffordPropertyPostCodePollingStationWebLookup-2017-02-10.csv'
    elections       = ['mayor.greater-manchester.2017-05-04']
