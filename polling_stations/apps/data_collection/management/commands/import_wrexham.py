from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'W06000006'
    addresses_name = 'WrexhamDemocracy_Club__04May2017 (2).tsv'
    stations_name = 'WrexhamDemocracy_Club__04May2017 (2).tsv'
    elections = [
        'local.wrexham.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'
