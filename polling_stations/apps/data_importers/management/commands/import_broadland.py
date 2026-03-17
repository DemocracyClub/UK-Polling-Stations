from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = "2026-05-07/2026-03-05T09:52:31.712540/Broadland District Council Polling Districts.csv"
    stations_name = "2026-05-07/2026-03-05T09:52:31.712540/Broadland District Council Polling Stations.csv"
    elections = ["2026-05-07"]
