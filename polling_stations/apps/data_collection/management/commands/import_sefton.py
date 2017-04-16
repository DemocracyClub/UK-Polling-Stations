from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000014'
    addresses_name = 'Democracy_Club__04May2017 Sefton.tsv'
    stations_name = 'Democracy_Club__04May2017 Sefton.tsv'
    elections = ['mayor.liverpool-city-ca.2017-05-04']
    csv_delimiter = '\t'
