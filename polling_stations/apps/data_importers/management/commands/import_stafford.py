from data_importers.management.commands import BaseHalaroseCsvImporter

FORTON_CRICKET_CLUB = {
    "pollingstationname": "Forton Cricket Club",
    "pollingstationaddress_1": "Eccleshall Road",
    "pollingstationaddress_2": "Forton",
    "pollingstationaddress_3": "Nr Newport",
    "pollingstationaddress_4": "Shropshire",
    "pollingstationaddress_5": "",
    "pollingstationpostcode": "TF10 8BF",
}


class Command(BaseHalaroseCsvImporter):
    council_id = "STA"
    addresses_name = "2024-07-04/2024-06-03T09:07:55.257705/STA_combined.csv"
    stations_name = "2024-07-04/2024-06-03T09:07:55.257705/STA_combined.csv"
    elections = ["2024-07-04"]

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
            "100031780034",  # 28 SANDON ROAD, STAFFORD
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

        station_hash = self.get_station_hash(record)

        # change from Council
        # old: Forton Village Hall
        # new: Forton Cricket Club
        if station_hash == "26-forton-village-hall":
            record = record._replace(**FORTON_CRICKET_CLUB)

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)

        # change from Council
        # old: Forton Village Hall
        # new: Forton Cricket Club
        if station_hash == "26-forton-village-hall":
            record = record._replace(**FORTON_CRICKET_CLUB)

        return super().station_record_to_dict(record)
