from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000153'
    addresses_name = 'Democracy_Club__04May2017 (Kettering).tsv'
    stations_name = 'Democracy_Club__04May2017 (Kettering).tsv'
    elections = [
        'local.northamptonshire.2017-05-04',
        'local.kettering.2017-05-04',
    ]
    csv_delimiter = '\t'
