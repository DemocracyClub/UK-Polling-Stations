from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "IOS"
    addresses_name = "2021-03-19T15:32:48.885694349/Democracy Club 2021 05 Scilly polling districts.csv"
    stations_name = "2021-03-19T15:32:48.885694349/Democracy Club 2021 05 Scilly polling stations.csv"
    elections = ["2021-05-06"]
