from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000105'
    addresses_name = 'Ashford_Democracy_Club__04May2017.CSV'
    stations_name = 'Ashford_Democracy_Club__04May2017.CSV'
    elections = [
        'local.kent.2017-05-04',
        'parl.2017-06-08'
    ]
