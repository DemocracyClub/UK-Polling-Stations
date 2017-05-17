from data_collection.management.commands import BaseXpressDCCsvInconsistentPostcodesImporter

class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = 'E07000171'
    addresses_name = 'Democracy_Club__04May2017 (7).tsv'
    stations_name = 'Democracy_Club__04May2017 (7).tsv'
    elections = [
        'local.nottinghamshire.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
