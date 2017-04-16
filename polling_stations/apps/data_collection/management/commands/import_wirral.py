from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000015'
    addresses_name = 'Democracy_Club__04May2017 (Wirral).tsv'
    stations_name = 'Democracy_Club__04May2017 (Wirral).tsv'
    elections = [
        'mayor.liverpool-city-ca.2017-05-04',
        'local.wirral.2017-05-04',
    ]
    csv_delimiter = '\t'
    csv_encoding = 'latin-1'
