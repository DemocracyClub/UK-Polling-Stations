from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000028'
    addresses_name = 'SandwellDemocracy_Club__04May2017 2.tsv'
    stations_name = 'SandwellDemocracy_Club__04May2017 2.tsv'
    elections = ['mayor.west-midlands.2017-05-04']
    csv_delimiter = '\t'
