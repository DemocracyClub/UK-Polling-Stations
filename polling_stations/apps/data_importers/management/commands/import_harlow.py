from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAR"
    addresses_name = (
        "2023-05-04/2023-03-03T09:41:36.035764/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-03T09:41:36.035764/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023420143",  # BENSONS, HARLOW COMMON, HARLOW
            "10023422799",  # BENSONS BARN, HARLOW COMMON, HARLOW
            "100091255381",  # KITCHEN HALL FARM, RED LION LANE, HARLOW
            "100091438137",  # 1 KITCHEN HALL COTTAGES, RED LION LANE, HARLOW
            "200002567081",  # CARETAKERS HOUSE KINGSMOOR COUNTY PRIMARY SCHOOL PLOYTERS ROAD, HARLOW
            "100091438138",  # 2 KITCHEN HALL COTTAGES, RED LION LANE, HARLOW
        ]:
            return None

        if record.addressline6 in [
            "CM20 1BA",  # split
            "CM20 2EP",  # HARLOW MILL LOCKHOUSE, CAMBRIDGE ROAD, HARLOW
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # St Thomas More Church Hall, Hodings Road, Harlow
        if rec["internal_council_id"] == "4390":
            rec["location"] = Point(0.080382, 51.770798, srid=4326)

        return rec
