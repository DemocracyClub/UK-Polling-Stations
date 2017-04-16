from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000029'
    addresses_name = 'Democracy_Club__04May2017 (Solihull).tsv'
    stations_name = 'Democracy_Club__04May2017 (Solihull).tsv'
    elections = ['mayor.west-midlands.2017-05-04']
    csv_delimiter = '\t'
