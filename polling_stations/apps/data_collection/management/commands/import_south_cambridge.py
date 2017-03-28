from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000012'
    addresses_name = 'May 2017/Democracy_Club__04May2017 (1).CSV'
    stations_name = 'May 2017/Democracy_Club__04May2017 (1).CSV'
    elections = [
        'local.cambridgeshire.2017-05-04',
        'mayor.cambridgeshire-and-peterborough.2017-05-04'
    ]
