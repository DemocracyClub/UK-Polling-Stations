from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BDF"
    addresses_name = (
        "2023-10-19/2023-09-18T14:25:44.359517/Democracy Club - PD-utf-8.csv"
    )
    stations_name = (
        "2023-10-19/2023-09-18T14:25:44.359517/Democracy Club - PS-utf-8.csv"
    )
    elections = ["2023-10-19"]
