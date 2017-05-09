from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000066'
    addresses_name = 'Giant TSV instead/BasildonDemocracy_Club__04May2017 (5).tsv'
    stations_name = 'Giant TSV instead/BasildonDemocracy_Club__04May2017 (5).tsv'
    elections = [
        'local.essex.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
