from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "WSM"
    addresses_name = "2026-05-07/2026-03-10T11:27:05.934023/Democracy Club - Idox_2026-03-10 10-57.csv"
    stations_name = "2026-05-07/2026-03-10T11:27:05.934023/Democracy Club - Idox_2026-03-10 10-57.csv"
    elections = ["2026-05-07"]
