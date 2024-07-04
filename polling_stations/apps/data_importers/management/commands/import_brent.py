from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BEN"
    addresses_name = "2024-07-04/2024-06-18T15:59:16.281758/BEN_PD_combined.csv"
    stations_name = "2024-07-04/2024-06-18T15:59:16.281758/BEN_PS_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "202033643",  # 164 WALM LANE, LONDON
            "202066948",  # 6 MOUNT PLEASANT, WEMBLEY
            "202196807",  # FLAT EAST LANE PAVILION EAST LANE, WEMBLEY
            "202030534",  # 101 WINCHESTER AVENUE, LONDON
        ]:
            return None

        if record.postcode in [
            # looks wrong
            "HA0 1WY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # removes wrong point for: Brent Hubs Kilburn Hornbill House 2 Rudolph Road London
        if record.stationcode in [
            "69",
            "70",
        ]:
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
