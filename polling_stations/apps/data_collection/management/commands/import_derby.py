from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000015'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 Derby City.TSV'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 Derby City.TSV'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
