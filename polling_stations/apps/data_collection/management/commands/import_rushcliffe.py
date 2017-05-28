from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000176'
    addresses_name = 'parl.2017-06-08/Version 1/Rushcliffe Democracy_Club__08June2017-Rushcliffe.TSV'
    stations_name = 'parl.2017-06-08/Version 1/Rushcliffe Democracy_Club__08June2017-Rushcliffe.TSV'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
