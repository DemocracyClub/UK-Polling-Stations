from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BEN"
    addresses_name = (
        "2024-07-04/2024-06-05T23:48:16.041079/DC -polling districts.csv 4 July.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-05T23:48:16.041079/DC -polling stations.csv 4 July.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

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
