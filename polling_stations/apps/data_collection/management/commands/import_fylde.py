from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E07000119'
    addresses_name  = 'parl.2017-06-08/Version 1/Fylde Democracy_Club__08June2017.CSV'
    stations_name   = 'parl.2017-06-08/Version 1/Fylde Democracy_Club__08June2017.CSV'
    elections       = ['parl.2017-06-08']
