from data_collection.management.commands import BaseXpressDCCsvInconsistentPostcodesImporter

class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = 'E06000056'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (2).tsv'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (2).tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
