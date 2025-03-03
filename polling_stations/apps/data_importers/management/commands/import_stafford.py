from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "STA"
    addresses_name = "2025-05-01/2025-03-03T11:42:30.038880/Eros_SQL_Output028.csv"
    stations_name = "2025-05-01/2025-03-03T11:42:30.038880/Eros_SQL_Output028.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200001329430",  # ENSON HOUSE, ENSON, STAFFORD
            "10023356767",  # TUDOR HOUSE ADJ TO 8 NEWPORT ROAD, WOOTTON, ECCLESHALL
            "100031782983",  # ACTON HILL FARM, ECCLESHALL, STAFFORD
            "100031768512",  # MOSS BYRE, GRUB STREET, HIGH OFFLEY, STAFFORD
            "200001318022",  # THE OLD LODGE, COTES, SWYNNERTON, STONE
            "10002085035",  # BARNSIDE, UTTOXETER ROAD, STONE
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
