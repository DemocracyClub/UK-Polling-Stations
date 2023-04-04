from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SNO"
    addresses_name = "2023-05-04/2023-04-04T11:27:01.256937/3DemocracyClub_PollingDistricts_040523.csv"
    stations_name = "2023-05-04/2023-04-04T11:27:01.256937/3DemocracyClub_PollingStations_04052023.csv"
    elections = ["2023-05-04"]
