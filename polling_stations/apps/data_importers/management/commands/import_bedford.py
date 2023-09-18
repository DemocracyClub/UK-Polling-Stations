from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BDF"
    addresses_name = "2023-10-19/2023-09-18T16:39:21.200794/districts.csv"
    stations_name = "2023-10-19/2023-09-18T16:39:21.200794/stations.csv"
    elections = ["2023-10-19"]
