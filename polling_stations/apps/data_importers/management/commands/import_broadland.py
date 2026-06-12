from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = "2026-07-16/2026-06-12T15:10:28.838687/Broadland District Council - polling districts.csv"
    stations_name = "2026-07-16/2026-06-12T15:10:28.838687/Broadland District Council - polling stations.csv"
    elections = ["2026-07-16"]
    csv_encoding = "utf-16le"
