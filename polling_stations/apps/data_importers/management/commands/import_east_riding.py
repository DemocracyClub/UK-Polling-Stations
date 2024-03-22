from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERY"
    addresses_name = "2024-05-02/2024-03-22T11:00:10.036289/Democracy Club - Polling Districts - PCC.csv"
    stations_name = "2024-05-02/2024-03-22T11:00:10.036289/Democracy Club - Polling Stations - PCC.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"
