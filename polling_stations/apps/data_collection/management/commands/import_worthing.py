from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000229'
    addresses_name = 'Democracy_Club__04May2017 WORTHING.TSV'
    stations_name = 'Democracy_Club__04May2017 WORTHING.TSV'
    elections = ['local.west-sussex.2017-05-04']
    csv_delimiter = '\t'
