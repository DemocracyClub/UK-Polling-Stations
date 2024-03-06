from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BEN"
    addresses_name = (
        "2024-05-02/2024-03-06T09:38:20.428353/Polling District  - Democracy Club.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-06T09:38:20.428353/Polling Stations - Democracy Club.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # point correction for: St Mary's Willesden Parish Church, Neasden Lane, London, NW10 2TS
        if record.stationcode == "ERW480":
            record = record._replace(yordinate="184797")
            record = record._replace(xordinate="521445")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "202033643",  # 164 WALM LANE, LONDON
            "202066948",  # 6 MOUNT PLEASANT, WEMBLEY
            "202196807",  # FLAT EAST LANE PAVILION EAST LANE, WEMBLEY
            "202030534",  # 101 WINCHESTER AVENUE, LONDON
            "202142340",  # 106 NORTON ROAD, WEMBLEY
            "202208354",  # 108 NORTON ROAD, WEMBLEY
        ]:
            return None

        if record.postcode in [
            # looks wrong
            "HA0 1WY",
        ]:
            return None

        return super().address_record_to_dict(record)
