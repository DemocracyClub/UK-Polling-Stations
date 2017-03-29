from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000181'
    addresses_name = 'May 2017/WestOxfordshire_Democracy_Club__04May2017.tsv'
    stations_name = 'May 2017/WestOxfordshire_Democracy_Club__04May2017.tsv'
    elections = ['local.oxfordshire.2017-05-04']
    csv_delimiter = '\t'
