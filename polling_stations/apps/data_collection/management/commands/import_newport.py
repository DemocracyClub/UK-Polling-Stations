from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'W06000022'
    addresses_name = 'Democracy_Club__04May2017_newport.tsv'
    stations_name = 'Democracy_Club__04May2017_newport.tsv'
    elections = ['local.newport.2017-05-04']
    csv_delimiter = '\t'
    csv_encoding = 'latin-1'
