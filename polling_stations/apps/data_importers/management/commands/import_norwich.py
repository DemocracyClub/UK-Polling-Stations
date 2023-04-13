from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = "2023-05-04/2023-04-13T15:24:40.310670/Democracy Club polling districts export.csv"
    stations_name = "2023-05-04/2023-04-13T15:24:40.310670/Democracy Club polling stations export.csv"
    elections = ["2023-05-04"]
