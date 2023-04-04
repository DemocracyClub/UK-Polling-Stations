from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = "2023-05-04/2023-04-04T11:19:44.580379/3DemocracyClub_PollingDistricts_040523.csv"
    stations_name = "2023-05-04/2023-04-04T11:19:44.580379/3DemocracyClub_PollingStations_04052023.csv"
    elections = ["2023-05-04"]
