from data_collection.management.commands import BaseDemocracyCountsCsvImporter

class Command(BaseDemocracyCountsCsvImporter):
    council_id = 'E07000095'
    addresses_name = 'local.2018-05-03/Version 1/Democracy Club - Polling Districts-2018- Broxbourne.csv'
    stations_name = 'local.2018-05-03/Version 1/Democracy Club - Polling Stations-2018 - Broxbourne 2.csv'
    elections = ['local.2018-05-03']
