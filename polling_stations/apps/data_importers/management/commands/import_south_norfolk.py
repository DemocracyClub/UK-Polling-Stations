from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SNO"
    addresses_name = "2026-05-07/2026-03-05T09:53:17.224658/South Norfolk Council Polling Districts.csv"
    stations_name = "2026-05-07/2026-03-05T09:53:17.224658/South Norfolk Council Polling Stations.csv"
    elections = ["2026-05-07"]
