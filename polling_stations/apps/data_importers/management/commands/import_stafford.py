from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "STA"
    addresses_name = "2021-03-18T11:55:59.579503/polling_station_export-2021-03-16.csv"
    stations_name = "2021-03-18T11:55:59.579503/polling_station_export-2021-03-16.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200001329430",  # ENSON HOUSE, ENSON, STAFFORD
            "10023358709",  # BEACON CROFT, BEACON FARM, BEACONSIDE, STAFFORD
            "10023356767",  # TUDOR HOUSE ADJ TO 8 NEWPORT ROAD, WOOTTON, ECCLESHALL
            "200001316894",  # 62 PERLE BROOK, ECCLESHALL, STAFFORD
            "200001316891",  # 23 PERLE BROOK, ECCLESHALL, STAFFORD
            "200001316890",  # 21 PERLE BROOK, ECCLESHALL, STAFFORD
            "200001316895",  # 64 PERLE BROOK, ECCLESHALL, STAFFORD
            "200001316892",  # 58 PERLE BROOK, ECCLESHALL, STAFFORD
            "200001316893",  # 60 PERLE BROOK, ECCLESHALL, STAFFORD
            "200001316889",  # 19 PERLE BROOK, ECCLESHALL, STAFFORD
            "100031777610",  # 17 PERLE BROOK, ECCLESHALL, STAFFORD
            "100031786273"  # CHASE COTTAGE, STAFFORD ROAD, ECCLESHALL, STAFFORD
            "200001329648",  # WOODRUFF BARN, BISHTON LANE, WOLSELEY BRIDGE, STAFFORD
        ]:
            return None

        if record.housepostcode in ["ST21 6NT", "ST17 0NU", "ST15 8SH"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Wedgwood Cricket Club Barlaston Park Barlaston Stoke on Trent ST12 9ES
        if (record.pollingstationnumber, record.pollingstationpostcode) == (
            "87",
            "ST12 9ES",
        ):
            record = record._replace(pollingstationpostcode="ST12 9ER")

        return super().station_record_to_dict(record)
