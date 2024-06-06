from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "IOS"
    addresses_name = (
        "2024-07-04/2024-06-06T11:29:05.281066/2024_07_Scilly_polling_districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T11:29:05.281066/2024_07_Scilly_polling_stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"
