from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000014'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 2.CSV'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 2.CSV'
    elections = ['parl.2017-06-08']
