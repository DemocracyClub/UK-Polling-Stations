from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000010'
    addresses_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
