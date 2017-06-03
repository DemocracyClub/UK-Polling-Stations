from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000228'
    addresses_name = 'parl.2017-06-08/Version 2/merged.csv'
    stations_name = 'parl.2017-06-08/Version 2/merged.csv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
