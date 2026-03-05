from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2026-05-07/2026-03-05T11:29:56.194818/20260305 Democracy Club Polling Districts.csv"
    stations_name = "2026-05-07/2026-03-05T11:29:56.194818/20260305 Democracy Club Polling Stations.csv"
    elections = ["2026-05-07"]
