from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000046'
    addresses_name = 'Democracy_Club__04May2017 (3).CSV'
    stations_name = 'Democracy_Club__04May2017 (3).CSV'
    elections = [
        'local.devon.2017-05-04',
        'parl.2017-06-08'
    ]
