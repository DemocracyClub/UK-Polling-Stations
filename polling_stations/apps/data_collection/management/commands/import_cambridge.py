from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000008'
    addresses_name  = 'parl.2017-06-08/Version 1/Cambridge_polling_station_export-2017-05-18_DemocracyClub.csv'
    stations_name   = 'parl.2017-06-08/Version 1/Cambridge_polling_station_export-2017-05-18_DemocracyClub.csv'
    elections       = ['parl.2017-06-08']
    csv_encoding    = 'latin-1'
