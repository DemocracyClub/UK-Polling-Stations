from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000145"
    addresses_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-12GY.csv"
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-12GY.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "28-methodist-church-hall":
            rec["location"] = Point(1.714309, 52.572677, srid=4326)
        if rec["internal_council_id"] == "38-methodist-hall":
            rec["location"] = Point(1.72571, 52.57462, srid=4326)

        # Corrections from Council
        if rec["internal_council_id"] == "11-the-priory-centre":
            rec["postcode"] = "NR30 1NA"
            rec["address"] = "The Catalyst\nThe Conge\nGreat Yarmouth"
        if rec["internal_council_id"] == "28-community-building":
            rec["postcode"] = "NR31 7ND"
            rec["address"] = "St Marys Church Hall\nFastolff Avenue\nGorleston"

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "100091323182":
            rec["postcode"] = "NR31 0DX"

        if record.houseid == "44678":
            return None

        if uprn == "10023461966":
            rec["postcode"] = "NR31 9HF"

        if record.housepostcode in ["NR31 6BA", "NR29 5HN", "NR29 5HN"]:
            return None

        if uprn in ["100091616205"]:
            rec["postcode"] = "NR29 4HZ"

        if uprn in [
            "10012182814",  # NR319TY -> NR319FH : 20 HERON WAY, KINGFISHER PARK, BUTT LANE, BURGH CASTLE, GREAT YARMOUTH
            "10023466148",  # NR305EL -> NR301EL : FLAT 6 DEXLYN COURT, 8 9 NORFOLK SQUARE, GREAT YARMOUTH
            "10012180406",  # NR294SL -> NR294JL : APHRODITE, 44 FAKES ROAD, NEWPORT, HEMSBY, GREAT YARMOUTH
            "10023460310",  # NR319PN -> NR319FN : 15 WAVENEY VALLEY HOLIDAY VILLAGE, BUTT LANE, BURGH CASTLE, GREAT YARMOUTH
            "10023467196",  # NR319AH -> NR316SG : 3 LOWESTOFT ROAD, HOPTON, GREAT YARMOUTH
        ]:
            rec["accept_suggestion"] = True

        return rec
