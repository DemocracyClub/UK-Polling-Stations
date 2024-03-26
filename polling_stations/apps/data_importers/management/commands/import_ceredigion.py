from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = (
        "2024-05-02/2024-03-26T15:55:08.555130/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-26T15:55:08.555130/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"
