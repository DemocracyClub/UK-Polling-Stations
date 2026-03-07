from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ESK"
    addresses_name = "2026-05-07/2026-03-04T14:10:09.553919/East Suffolk Council - Polling Districts 07.05.26 - Unopened.csv"
    stations_name = "2026-05-07/2026-03-04T14:10:09.553919/East Suffolk Council - Polling Stations 07.05.26 - Unopened.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
