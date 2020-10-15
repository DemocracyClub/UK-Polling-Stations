from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000007"
    addresses_name = "parl.2019-12-12/Version 1/Democracy Club Polling Districts.csv"
    stations_name = "parl.2019-12-12/Version 1/Democracy Club Polling Stations.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False
