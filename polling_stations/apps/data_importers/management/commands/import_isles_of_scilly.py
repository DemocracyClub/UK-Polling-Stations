from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "IOS"
    addresses_name = (
        "2024-05-02/2024-04-16T18:51:35.252695/2024_05_Scilly_polling_districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-04-16T18:51:35.252695/2024_05_Scilly_polling_stations.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # splits
            "TR21 0AB"
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: Old Wesleyan Chapel, Old Wesleyan Chapel (rear entrance), Garrison Lane, St Mary's, Isles of Scilly, TR21 0JD
        if record.pollingstationid == "36":
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        return super().station_record_to_dict(record)
