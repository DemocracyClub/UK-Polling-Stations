from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000008'
    addresses_name  = 'Cambridge_polling_station_export_DemocracyClub.csv'
    stations_name   = 'Cambridge_polling_station_export_DemocracyClub.csv'
    elections       = [
        'local.cambridgeshire.2017-05-04'
        'mayor.cambridgeshire-and-peterborough.2017-05-04',
    ]
    csv_encoding    = 'latin-1'
