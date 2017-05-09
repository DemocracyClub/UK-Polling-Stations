from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000102'
    addresses_name = 'ThreeRiversDemocracy_Club__04May2017.tsvClub__04May2017.tsv'
    stations_name = 'ThreeRiversDemocracy_Club__04May2017.tsvClub__04May2017.tsv'
    elections = [
        'local.hertfordshire.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
    csv_encoding = 'latin-1'
