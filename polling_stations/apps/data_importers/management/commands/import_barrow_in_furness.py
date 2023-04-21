from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAR"
    addresses_name = (
        "2023-05-04/2023-04-21T14:38:15/Democracy_Club_-_Polling_DistrictsOBandH.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-21T14:38:15/Democracy_Club_Polling_Stations_OBandH.csv"
    )
    elections = ["2023-05-04"]
