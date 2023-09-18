from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CBF"
    addresses_name = (
        "2023-10-19/2023-09-18T15:14:23.313921/Democracy Club - PD-utf-8.csv"
    )
    stations_name = (
        "2023-10-19/2023-09-18T15:14:23.313921/Democracy Club - PS-utf-8.csv"
    )
    elections = ["2023-10-19"]
