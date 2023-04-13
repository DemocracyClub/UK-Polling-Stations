from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STV"
    addresses_name = "2023-05-04/2023-04-13T15:19:32.991038/Democracy Club - Polling Districts 4 May 2023.csv"
    stations_name = "2023-05-04/2023-04-13T15:19:32.991038/Democracy Club - Polling Stations 4 May 2023.csv"
    elections = ["2023-05-04"]
