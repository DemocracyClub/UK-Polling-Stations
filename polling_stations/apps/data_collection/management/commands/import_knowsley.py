from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000011'
    addresses_name = 'Democracy_Club__04May2017 - Knowsley MBC.CSV'
    stations_name = 'Democracy_Club__04May2017 - Knowsley MBC.CSV'
    elections = ['mayor.liverpool-city-ca.2017-05-04']
