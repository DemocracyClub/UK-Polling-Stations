from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "KTT"
    addresses_name = "2026-05-07/2026-03-17T09:05:17.344225/RBK - Polling Districts.csv"
    stations_name = "2026-05-07/2026-03-17T09:05:17.344225/RBK - Polling Stations.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
