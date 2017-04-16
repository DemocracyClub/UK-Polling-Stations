from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000214'
    addresses_name = 'Democracy_Club__04May2017 Surrey Heath.tsv'
    stations_name = 'Democracy_Club__04May2017 Surrey Heath.tsv'
    elections = ['local.surrey.2017-05-04']
    csv_delimiter = '\t'
