from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000047'
    addresses_name = 'parl.2017-06-08/Version 2/merged.tsv'
    stations_name = 'parl.2017-06-08/Version 2/merged.tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
