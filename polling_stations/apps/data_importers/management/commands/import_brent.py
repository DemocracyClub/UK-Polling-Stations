from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BEN"
    addresses_name = "2025-02-18/2025-01-27T15:00:43.238818/Democracy club Alperton by election Polling Districts.csv"
    stations_name = (
        "2025-02-18/2025-01-27T15:00:43.238818/Democracy club Alperton by election.csv"
    )
    elections = ["2025-02-18"]
    csv_encoding = "utf-16le"

    # Maintaining GE exclusions as the comment below for future reference

    # def address_record_to_dict(self, record):
    #     uprn = record.uprn.strip().lstrip("0")
    #     if uprn in [
    #         "202033643",  # 164 WALM LANE, LONDON
    #         "202066948",  # 6 MOUNT PLEASANT, WEMBLEY
    #         "202196807",  # FLAT EAST LANE PAVILION EAST LANE, WEMBLEY
    #         "202030534",  # 101 WINCHESTER AVENUE, LONDON
    #     ]:
    #         return None

    #     if record.postcode in [
    #         # looks wrong
    #         "HA0 1WY",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)

    # def station_record_to_dict(self, record):
    #     # removes wrong point for: Brent Hubs Kilburn Hornbill House 2 Rudolph Road London
    #     if record.stationcode in [
    #         "69",
    #         "70",
    #     ]:
    #         record = record._replace(xordinate="", yordinate="")

    #     return super().station_record_to_dict(record)
