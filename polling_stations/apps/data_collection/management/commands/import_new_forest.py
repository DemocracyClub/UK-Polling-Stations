from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000091'
    addresses_name = 'New better data for 4 May 2017/Democracy_Club__04May2017 (4)-fixed.tsv'
    stations_name = 'New better data for 4 May 2017/Democracy_Club__04May2017 (4)-fixed.tsv'
    elections = ['local.hampshire.2017-05-04']
    csv_delimiter = '\t'
    csv_encoding = 'windows-1252'
