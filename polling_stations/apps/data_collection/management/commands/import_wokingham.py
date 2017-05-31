from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000041'
    addresses_name = 'parl.2017-06-08/Version 1/merged.tsv'
    stations_name = 'parl.2017-06-08/Version 1/merged.tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
