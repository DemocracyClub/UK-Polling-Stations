from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000010'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (20).tsv'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (20).tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
