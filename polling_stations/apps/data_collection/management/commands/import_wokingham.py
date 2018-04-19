from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000041'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Wokingham.csv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Wokingham.csv'
    elections = ['local.2018-05-03']
    csv_delimiter = ','
