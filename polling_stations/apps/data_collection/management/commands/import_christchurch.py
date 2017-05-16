from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000048'
    addresses_name = 'parl.2017-06-08/Version 1/201705`4 Democracy_Club__08June2017 Export - Christchurch Borough Council.TSV'
    stations_name = 'parl.2017-06-08/Version 1/201705`4 Democracy_Club__08June2017 Export - Christchurch Borough Council.TSV'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
