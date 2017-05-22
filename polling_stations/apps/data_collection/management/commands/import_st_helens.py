from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000013'
    addresses_name = 'parl.2017-06-08/Version 1/St. Helen\'s Democracy_Club__08June2017 2.tsv'
    stations_name = 'parl.2017-06-08/Version 1/St. Helen\'s Democracy_Club__08June2017 2.tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
