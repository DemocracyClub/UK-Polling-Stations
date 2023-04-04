from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2023-05-04/2023-04-04T11:13:30.818764/Democracy club - 2nd attempt - polling districts 4-5-2023.csv"
    stations_name = "2023-05-04/2023-04-04T11:13:30.818764/Democracy Club - 2nd attempt - polling stations 4-5-2023.csv"
    elections = ["2023-05-04"]
