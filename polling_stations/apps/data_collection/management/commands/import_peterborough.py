from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000031'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (1).tsvv'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (1).tsvv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
    csv_encoding = 'latin-1'
