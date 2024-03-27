from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SNO"
    addresses_name = "2024-05-02/2024-03-27T14:48:36.251363/SNC Democracy Club_Polling Districts .csv"
    stations_name = (
        "2024-05-02/2024-03-27T14:48:36.251363/SNC Democracy Club_Polling Stations .csv"
    )
    elections = ["2024-05-02"]
