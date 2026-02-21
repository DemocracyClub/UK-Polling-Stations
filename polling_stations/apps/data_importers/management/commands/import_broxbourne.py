from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2026-05-07/2026-02-17T17:40:08.019036/Democracy club- polling districts for Borough of Broxbourne 7-5-2026.csv"
    stations_name = "2026-05-07/2026-02-17T17:40:08.019036/Democracy club- polling stations for Borough of Broxbourne 7-5-2026.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"
