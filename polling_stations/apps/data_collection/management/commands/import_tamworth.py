from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000199'
    addresses_name = 'TamworthDemocracy_Club__04May2017 (2).tsv'
    stations_name = 'TamworthDemocracy_Club__04May2017 (2).tsv'
    elections = ['local.staffordshire.2017-05-04']
    csv_delimiter = '\t'
