from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CBF"
    addresses_name = "2023-10-19/2023-09-18T16:40:13.338932/districts.csv"
    stations_name = "2023-10-19/2023-09-18T16:40:13.338932/stations.csv"
    elections = ["2023-10-19"]
