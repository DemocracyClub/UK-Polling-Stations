from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000242'
    addresses_name = 'Democracy_Club__04May2017 (5).CSV'
    stations_name = 'Democracy_Club__04May2017 (5).CSV'
    elections = [
        'local.hertfordshire.2017-05-04',
        'local.east-hertfordshire.2017-05-04',
        'parl.2017-06-08'
    ]
