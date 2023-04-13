from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ESK"
    addresses_name = "2023-05-04/2023-04-13T15:35:25.165461/East Suffolk Council - Democracy Club - Polling Districts May 2023.csv"
    stations_name = "2023-05-04/2023-04-13T15:35:25.165461/East Suffolk Council - Democracy Club - Polling Stations May 2023.csv"
    elections = ["2023-05-04"]
