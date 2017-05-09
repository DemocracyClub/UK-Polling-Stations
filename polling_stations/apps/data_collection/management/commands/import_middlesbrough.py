from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000002'
    addresses_name = 'Democracy_Club__04May2017 (6).tsv'
    stations_name = 'Democracy_Club__04May2017 (6).tsv'
    elections = [
        'mayor.tees-valley.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
