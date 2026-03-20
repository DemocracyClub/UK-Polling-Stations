from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "CLK"
    addresses_name = "2026-05-07/2026-03-20T15:50:17.482256/Democracy Club Clackmannanshire and Dunblane - Idox_2026-03-20 15-48.csv"
    stations_name = "2026-05-07/2026-03-20T15:50:17.482256/Democracy Club Clackmannanshire and Dunblane - Idox_2026-03-20 15-48.csv"
    elections = ["2026-05-07"]
