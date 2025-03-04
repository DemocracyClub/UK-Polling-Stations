from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "IOS"
    addresses_name = (
        "2025-05-01/2025-03-04T13:19:08.206991/2025_05_Scilly_polling_districts.csv"
    )
    stations_name = (
        "2025-05-01/2025-03-04T13:19:08.206991/2025_05_Scilly_polling_stations.csv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
