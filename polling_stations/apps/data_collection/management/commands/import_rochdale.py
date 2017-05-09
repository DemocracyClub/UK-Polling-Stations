from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E08000005'
    addresses_name  = 'Rochdale_Democracy_Club__04May2017 (2).CSV'
    stations_name   = 'Rochdale_Democracy_Club__04May2017 (2).CSV'
    elections       = [
        'mayor.greater-manchester-ca.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = ','
