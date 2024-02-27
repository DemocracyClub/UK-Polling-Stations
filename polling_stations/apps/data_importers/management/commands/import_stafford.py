from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "STA"
    addresses_name = "2024-05-02/2024-02-27T09:37:25.220071/Eros_SQL_Output020.csv"
    stations_name = "2024-05-02/2024-02-27T09:37:25.220071/Eros_SQL_Output020.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200001329430",  # ENSON HOUSE, ENSON, STAFFORD
            "10023358709",  # BEACON CROFT, BEACON FARM, BEACONSIDE, STAFFORD
            "10023356767",  # TUDOR HOUSE ADJ TO 8 NEWPORT ROAD, WOOTTON, ECCLESHALL
            "100031782983",  # ACTON HILL FARM, ECCLESHALL, STAFFORD
            "100031768512",  # MOSS BYRE, GRUB STREET, HIGH OFFLEY, STAFFORD
            "200001318022",  # THE OLD LODGE, COTES, SWYNNERTON, STONE
            "10002085035",  # BARNSIDE, UTTOXETER ROAD, STONE
            "200001327641",  # LIVING ACCOMMODATION HOP POLE 22 SANDON ROAD, STAFFORD
            "10002090418",  # OAKFIELD HOUSE, THE OLD FRUIT FARM, FRADSWELL, STAFFORD
        ]:
            return None

        if record.housepostcode in [
            # split
            "ST17 0NU",
            # suspect
            "ST21 6AN",
            "ST21 6BE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Wedgwood Cricket Club Barlaston Park Barlaston Stoke on Trent ST12 9ES
        if (record.pollingstationnumber) == "1029":
            record = record._replace(pollingstationpostcode="ST12 9ER")

        return super().station_record_to_dict(record)
