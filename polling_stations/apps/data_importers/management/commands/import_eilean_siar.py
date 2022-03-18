from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ELS"
    addresses_name = "2022-05-05/2022-03-18T12:34:38.484076/WI Democracy Club - Polling Districts.csv"
    stations_name = (
        "2022-05-05/2022-03-18T12:34:38.484076/WI Democracy Club - Polling Stations.csv"
    )
    elections = ["2022-05-05"]
