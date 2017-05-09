from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000139'
    addresses_name = 'Democracy_Club export for NKDC__04May2017.tsv'
    stations_name = 'Democracy_Club export for NKDC__04May2017.tsv'
    elections = [
        'local.lincolnshire.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
    csv_encoding  = 'latin-1'
