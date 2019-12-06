from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E06000012"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-27NELC.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-27NELC.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode.strip() == "DN333 3E":
            rec["postcode"] = "DN33 3EN"

        if record.housepostcode.strip() in ["DN35 8AB", "DN33 2AD"]:
            return None

        if uprn == "10090082509":
            return None

        if uprn in [
            "11073783"  # DN364QR -> DN364QQ : 298 STATION ROAD, NEW WALTHAM, NORTH EAST LINCOLNSHIRE
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "11073743",  # DN364RX -> DN364RY : THE BUNGALOW WALTHAM HOUSE LOUTH ROAD, WALTHAM, NORTH EAST LINCOLNSHIRE
            "11076295",  # DN357AB -> DN357HE : GROUND FLOOR REAR FLAT 22 GRIMSBY ROAD, CLEETHORPES, NORTH EAST LINCOLNSHIRE
            "11019854",  # DN370HU -> DN370JA : BRIAR FARM CHEAPSIDE, WALTHAM, NORTH EAST LINCOLNSHIRE
            "11053301",  # DN370HU -> DN370HT : BRIGSLEY TOP FARM CHEAPSIDE, WALTHAM, NORTH EAST LINCOLNSHIRE
        ]:
            rec["accept_suggestion"] = False

        return rec
