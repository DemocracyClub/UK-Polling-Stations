from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "VGL"
    addresses_name = (
        "2024-05-02/2024-03-22T16:08:51.555473/Democracy Club Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-22T16:08:51.555473/Democracy Club Polling Stations.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"
