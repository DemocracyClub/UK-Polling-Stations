from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000201'
    addresses_name = 'Forest_Heath_split.csv'
    stations_name = 'Forest_Heath_split.csv'
    elections = ['local.suffolk.2017-05-04']
