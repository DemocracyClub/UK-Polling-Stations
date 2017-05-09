from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000047'
    addresses_name = 'Democracy_Club__04May2017 - west devon.TSV'
    stations_name = 'Democracy_Club__04May2017 - west devon.TSV'
    elections = [
        'local.devon.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
