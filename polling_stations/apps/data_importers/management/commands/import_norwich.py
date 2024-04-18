from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = "2024-05-02/2024-03-18T08:50:17.047358/Democracy Club - Polling Districts export.csv"
    stations_name = "2024-05-02/2024-03-18T08:50:17.047358/Democracy Club - 2024 Polling Stations export 4.csv"
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # Coordinate change from council for: ST ALBAN'S CHURCH HALL, GROVE WALK, NORWICH
        if record.stationcode in ("48TO5", "46TO3"):
            record = record._replace(
                xordinate="622820",
                yordinate="307543",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10024023874",  # LIVING ACCOMMODATION THE MARSH HARRIER IPSWICH ROAD, NORWICH
            "200004349456",  # 14A IPSWICH ROAD, NORWICH
        ]:
            return None

        return super().address_record_to_dict(record)
