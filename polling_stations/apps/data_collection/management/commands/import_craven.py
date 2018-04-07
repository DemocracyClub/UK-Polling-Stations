from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000163'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Craven.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Craven.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
    csv_encoding = 'windows-1252'
