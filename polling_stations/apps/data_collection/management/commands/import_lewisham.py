from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000023'
    addresses_name = 'parl.lewisham-east.by.2018-06-14/Version 1/Democracy_Club__14June2018.tsv'
    stations_name = 'parl.lewisham-east.by.2018-06-14/Version 1/Democracy_Club__14June2018.tsv'
    elections = ['parl.lewisham-east.by.2018-06-14']
    csv_delimiter = '\t'
