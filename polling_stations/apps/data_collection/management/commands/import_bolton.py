from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000001'
    addresses_name = 'Democracy_Club__04May2017_Bolton.CSV'
    stations_name = 'Democracy_Club__04May2017_Bolton.CSV'
    elections = [
        'mayor.greater-manchester-ca.2017-05-04',
        'parl.2017-06-08'
    ]
