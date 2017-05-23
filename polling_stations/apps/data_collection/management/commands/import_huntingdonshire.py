from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000011'
    addresses_name = 'Hunts_Democracy_Club__04May2017.tsv'
    stations_name = 'Hunts_Democracy_Club__04May2017.tsv'
    """elections = [
        'mayor.cambridgeshire-and-peterborough.2017-05-04',
        'parl.2017-06-08'
    ]"""
    csv_delimiter = '\t'
