from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000145"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-25G Yar.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-25G Yar.csv"
    )
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "28-methodist-church-hall":
            rec["location"] = Point(1.714309, 52.572677, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "100091323182":
            rec["postcode"] = "NR31 0DX"

        if uprn == "10023461966":
            rec["postcode"] = "NR31 9HF"

        if record.houseid == "48125":
            rec["postcode"] = "NR31 9EP"

        if uprn == "100091559681":
            rec["postcode"] = "NR29 3PF"

        if uprn == "10012179821":
            rec["postcode"] = "NR30 3LD"

        if uprn == "10012182400":
            rec["postcode"] = "NR31 9EB"

        if record.houseid == "46097":
            rec["postcode"] = "NR31 6LP"

        if uprn in ["100091318449", "100091616205"]:
            rec["postcode"] = "NR29 4HZ"

        if record.houseid == "48177":
            rec["postcode"] = "NR31 6SG"  # NR31 9AH

        if record.houseid == "48376":
            rec["postcode"] = "NR31 6QT"  # NR30 2JT

        if record.houseid == "48841":
            rec["postcode"] = "NR30 3AY"  # NR30 5AY

        if uprn in [
            "10012182814",  # NR319TY -> NR319FH : 20 HERON WAY, KINGFISHER PARK, BUTT LANE, BURGH CASTLE, GREAT YARMOUTH
            "10023466148",  # NR305EL -> NR301EL : FLAT 6 DEXLYN COURT, 8 9 NORFOLK SQUARE, GREAT YARMOUTH
            "10012180406",  # NR294SL -> NR294JL : APHRODITE, 44 FAKES ROAD, NEWPORT, HEMSBY, GREAT YARMOUTH
            "100091616205",  # NR293NF -> NR294HZ : 285 BELLE AIRE, BEACH ROAD, HEMSBY, GREAT YARMOUTH
            "10023460310",  # NR319PN -> NR319FN : 15 WAVENEY VALLEY HOLIDAY VILLAGE, BUTT LANE, BURGH CASTLE, GREAT YARMOUTH
            "10023467196",  # NR319AH -> NR316SG : 3 LOWESTOFT ROAD, HOPTON, GREAT YARMOUTH
        ]:
            rec["accept_suggestion"] = True

        return rec
