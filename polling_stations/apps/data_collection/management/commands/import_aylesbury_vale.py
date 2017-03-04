from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id = 'E07000004'
    addresses_name = '2017/AylesburyValePropertyPostCodePollingStationWebLookup-2017-03-02 2.TSV'
    stations_name = '2017/AylesburyValePropertyPostCodePollingStationWebLookup-2017-03-02 2.TSV'
    elections = ['local.buckinghamshire.2017-05-04']
    csv_delimiter = '\t'
