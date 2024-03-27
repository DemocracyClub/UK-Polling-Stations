from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = "2024-05-02/2024-03-27T14:47:42.949549/BDC Democracy Club_Polling Districts .csv"
    stations_name = (
        "2024-05-02/2024-03-27T14:47:42.949549/BDC Democracy Club_Polling Stations .csv"
    )
    elections = ["2024-05-02"]
