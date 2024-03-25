from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ECA"
    addresses_name = "2024-05-02/2024-03-25T16:59:04.074992/Democracy Club - Polling Districts 2024.csv"
    stations_name = "2024-05-02/2024-03-25T16:59:04.074992/Polling Stations 2024.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"
