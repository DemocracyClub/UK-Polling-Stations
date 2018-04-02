from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000223'
    addresses_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018ADURresp.tsv'
    stations_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018ADURresp.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
