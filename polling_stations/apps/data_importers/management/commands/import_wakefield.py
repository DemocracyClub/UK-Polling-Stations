from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2023-05-04/2023-04-04T11:04:06.375522/20230320_DemocracyClubPollingDistricts_DistrictElections4May2023.csv"
    stations_name = "2023-05-04/2023-04-04T11:04:06.375522/20230320_DemocracyClubPollingStations_DistrictElections4May2023.csv"
    elections = ["2023-05-04"]
