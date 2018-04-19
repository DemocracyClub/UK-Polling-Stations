from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E07000099'
    addresses_name  = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 North Hertfordshire (2).tsv'
    stations_name   = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 North Hertfordshire (2).tsv'
    elections       = ['local.2018-05-03']
    csv_delimiter = '\t'
