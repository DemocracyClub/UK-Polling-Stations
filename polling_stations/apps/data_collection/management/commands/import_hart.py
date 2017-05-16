from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000089'
    addresses_name = 'parl.2017-06-08/Version 1/Hart DC General Election polling place 120517.TSV'
    stations_name = 'parl.2017-06-08/Version 1/Hart DC General Election polling place 120517.TSV'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
