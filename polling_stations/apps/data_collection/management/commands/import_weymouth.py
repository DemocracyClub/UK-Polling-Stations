from data_collection.management.commands import BaseXpressDCCsvInconsistentPostcodesImporter

class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = 'E07000053'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017WPBC.TSV'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017WPBC.TSV'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'
