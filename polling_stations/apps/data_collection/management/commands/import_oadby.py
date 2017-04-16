from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000135'
    addresses_name = 'Democracy_Club__04May2017 (Oadby & Wigston).tsv'
    stations_name = 'Democracy_Club__04May2017 (Oadby & Wigston).tsv'
    elections = ['local.leicestershire.2017-05-04']
    csv_delimiter = '\t'
