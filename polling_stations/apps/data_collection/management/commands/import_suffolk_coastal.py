from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000205'
    addresses_name  = 'Giant CSV instead/SuffolkCoastalpolling_station_export-2017-04-04.csv'
    stations_name   = 'Giant CSV instead/SuffolkCoastalpolling_station_export-2017-04-04.csv'
    elections       = ['local.suffolk.2017-05-04']
