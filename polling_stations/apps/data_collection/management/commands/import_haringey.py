from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000014'
    addresses_name = 'parl.2017-06-08/Version 2/Democracy_Club__08June2017 10.tsv'
    stations_name = 'parl.2017-06-08/Version 2/Democracy_Club__08June2017 10.tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
