from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000042'
    addresses_name = 'MidDevon_Democracy_Club__04May2017.tsv'
    stations_name = 'MidDevon_Democracy_Club__04May2017.tsv'
    elections = [
        'local.devon.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
