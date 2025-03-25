from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "OXO"
    addresses_name = "2025-05-01/2025-03-25T12:23:22.273024/Eros_SQL_Output003.csv"
    stations_name = "2025-05-01/2025-03-25T12:23:22.273024/Eros_SQL_Output003.csv"
    elections = ["2025-05-01"]

    def station_record_to_dict(self, record):
        # Littlemore Community Centre, Giles Road
        if self.get_station_hash(record) in [
            "47-littlemore-community-centre",
        ]:
            record = record._replace(pollingstationpostcode="OX4 4NW")

        rec = super().station_record_to_dict(record)

        # more accurate point for St Alban's Hall
        if rec["internal_council_id"] in (
            "39-st-albans-hall",
            "40-st-albans-hall",
        ):
            rec["location"] = Point(-1.232920, 51.740993, srid=4326)

        # and for Oxford Centre for Mission Studies
        if rec["internal_council_id"] in (
            "13-oxford-centre-for-mission-studies",
            "14-oxford-centre-for-mission-studies",
        ):
            rec["location"] = Point(-1.264263, 51.764185, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100121367548",  # ST. ANTONY'S COLLEGE, 62 WOODSTOCK ROAD, OXFORD
        ]:
            return None

        if record.housepostcode in [
            # split
            "OX3 0TX",
            "OX4 4UU",
            "OX1 4AQ",
            # suspect
            "OX2 7AH",  # narrowboats
        ]:
            return None
        return super().address_record_to_dict(record)
