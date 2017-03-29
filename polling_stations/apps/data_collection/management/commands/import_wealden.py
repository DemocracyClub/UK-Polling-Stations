from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000065'
    addresses_name = 'May 2017/Wealden_Democracy_Club__04May2017 (2).tsv'
    stations_name = 'May 2017/Wealden_Democracy_Club__04May2017 (2).tsv'
    elections = ['local.east-sussex.2017-05-04']
    csv_delimiter = '\t'
