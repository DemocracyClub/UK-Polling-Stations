from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STV"
    addresses_name = "2024-05-02/2024-02-28T10:22:00.393556/Democracy Club - Polling Districts 2 May 2024.csv"
    stations_name = "2024-05-02/2024-02-28T10:22:00.393556/Democracy Club - Polling Stations 2 May 2024.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"
