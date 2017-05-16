from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000049'
    addresses_name = 'parl.2017-06-08/Version 1/20170514 Democracy_Club__08June2017 Export - East Dorset District Council.TSV'
    stations_name = 'parl.2017-06-08/Version 1/20170514 Democracy_Club__08June2017 Export - East Dorset District Council.TSV'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
