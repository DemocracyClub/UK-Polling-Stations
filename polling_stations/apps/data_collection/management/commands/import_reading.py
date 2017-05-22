from data_collection.management.commands import BaseXpressDCCsvInconsistentPostcodesImporter

class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = 'E06000038'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (17).tsv'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (17).tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
