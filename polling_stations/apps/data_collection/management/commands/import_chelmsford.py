from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000070'
    addresses_name = 'Democracy_Club__04May2017 (1).tsv'
    stations_name = 'Democracy_Club__04May2017 (1).tsv'
    elections = [
        'local.essex.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
    csv_encoding = 'latin-1'
