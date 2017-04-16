from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000176'
    addresses_name = 'Democracy_Club__04May2017 (5).tsv'
    stations_name = 'Democracy_Club__04May2017 (5).tsv'
    elections = [
        'local.nottinghamshire.2017-05-04',
        'local.rushcliffe.2017-05-04',
    ]
    csv_delimiter = '\t'
