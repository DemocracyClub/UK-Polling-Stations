from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000031'
    addresses_name = 'Democracy_Club__04May2017_peterborough.tsv'
    stations_name = 'Democracy_Club__04May2017_peterborough.tsv'
    elections = ['mayor.cambridgeshire-and-peterborough.2017-05-04']
    csv_delimiter = '\t'
    csv_encoding = 'latin-1'
