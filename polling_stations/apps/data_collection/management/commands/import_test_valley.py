from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000093'
    addresses_name = 'TestValleyDemocracy_Club__04May2017 (2).tsv'
    stations_name = 'TestValleyDemocracy_Club__04May2017 (2).tsv'
    elections = [
        'local.hampshire.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
    csv_encoding = 'latin-1'
