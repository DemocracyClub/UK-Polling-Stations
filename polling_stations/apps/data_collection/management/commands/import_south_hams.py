from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000044'
    addresses_name = 'Democracy_Club__04May2017 - south hams.tsv'
    stations_name = 'Democracy_Club__04May2017 - south hams.tsv'
    elections = ['local.devon.2017-05-04']
    csv_delimiter = '\t'
