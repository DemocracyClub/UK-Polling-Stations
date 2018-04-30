from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000031'
    addresses_name = 'local.2018-05-03/Version 1/Democracry Club Polling Place Lookup - City Elections - 3 May 2018 - Peterborough City Council.TSV'
    stations_name = 'local.2018-05-03/Version 1/Democracry Club Polling Place Lookup - City Elections - 3 May 2018 - Peterborough City Council.TSV'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
    csv_encoding = 'windows-1252'
