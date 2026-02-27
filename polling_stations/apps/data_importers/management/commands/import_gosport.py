from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "GOS"
    addresses_name = "2026-05-07/2026-02-27T10:00:28.959884/GOS_districts_UTF8.csv"
    stations_name = "2026-05-07/2026-02-27T10:00:28.959884/GOS_stations_UTF8.csv"
    elections = ["2026-05-07"]
