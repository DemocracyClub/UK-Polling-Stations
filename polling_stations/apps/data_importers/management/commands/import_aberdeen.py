from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABE"
    addresses_name = "2026-06-25/2026-06-19T13:19:06.633385/Democracy Club - Idox_2026-05-14 17-14 (1).csv"
    stations_name = "2026-06-25/2026-06-19T13:19:06.633385/Democracy Club - Idox_2026-05-14 17-14 (1).csv"
    elections = ["2026-06-25"]
