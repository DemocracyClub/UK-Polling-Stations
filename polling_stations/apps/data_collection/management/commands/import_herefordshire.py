from data_collection.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "E06000019"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08here.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08here.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if record.pollingstationname == "Weobley Village Hall":
            rec["location"] = Point(-2.869103, 52.159915, srid=4326)

        if record.pollingstationname == "Richards Castle Village Hall":
            rec["location"] = Point(-2.74213, 52.32607, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode.strip() == "HR9 7RA":
            return None

        if uprn in ["10007369349", "10091655370"]:

            return None

        if record.houseid in [
            "3072006",
            "9010513",
        ]:
            return None

        if record.housepostcode.strip() in ["HR1 2PJ", "HR4 8FH"]:
            return None

        return rec
