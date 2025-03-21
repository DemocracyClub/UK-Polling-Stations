from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAR"
    addresses_name = (
        "2024-07-04/2024-06-11T15:09:04.858716/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-11T15:09:04.858716/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10023420143",  # BENSONS, HARLOW COMMON, HARLOW
                "10023422799",  # BENSONS BARN, HARLOW COMMON, HARLOW
                "100091255381",  # KITCHEN HALL FARM, RED LION LANE, HARLOW
                "100091438137",  # 1 KITCHEN HALL COTTAGES, RED LION LANE, HARLOW
                "100091438138",  # 2 KITCHEN HALL COTTAGES, RED LION LANE, HARLOW
                "100091255475",  # NEXUS HOUSE, SCHOOL LANE, HARLOW
                "200002567135",  # STEWARDS RESIDENCE CANONS BROOK GOLF CLUB ELIZABETH WAY, HARLOW
                "10003710616",  # HEART & CLUB, PYPERS HATCH, HARLOW
                "100091255570",  # GOLDINGS FARM, TYE GREEN VILLAGE, HARLOW
                "100091255180",  # THE HAWTHORNS, MONKSWICK ROAD, HARLOW
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "CM20 1BA",
            # looks wrong
            "CM20 3QF",
            "CM20 3RA",
            "CM20 3PA",
            "CM20 3RL",
            "CM19 4EU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # St Thomas More Church Hall, Hodings Road, Harlow
        if rec["internal_council_id"] == "4820":
            rec["location"] = Point(0.080382, 51.770798, srid=4326)

        return rec
