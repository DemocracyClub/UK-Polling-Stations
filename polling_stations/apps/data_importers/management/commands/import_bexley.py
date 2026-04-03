from data_importers.management.commands import Unknown


class Command(Unknown):
    council_id = "BEX"
    addresses_name = "2026-05-07/2026-03-20T14:23:56.396389/Polling stations.csv"
    stations_name = "2026-05-07/2026-03-20T14:23:56.396389/Polling stations.csv"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
