from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2026-05-07/2026-03-17T09:06:50.410836/20260305 Democracy Club Polling Districts_UTF8.csv"
    stations_name = "2026-05-07/2026-03-17T09:06:50.410836/20260305 Democracy Club Polling Stations.csv"
    elections = ["2026-05-07"]
