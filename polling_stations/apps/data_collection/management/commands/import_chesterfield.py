from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000034'
    addresses_name = 'May 2017/ChesterfieldDemocracy_Club__04May2017a.txt'
    stations_name = 'May 2017/ChesterfieldDemocracy_Club__04May2017a.txt'
    elections = ['local.derbyshire.2017-05-04']
    csv_delimiter = '\t'
