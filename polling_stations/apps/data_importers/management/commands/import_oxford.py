from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "OXO"
    addresses_name = "2024-07-04/2024-06-14T14:48:51.773461/OXO_combined.csv"
    stations_name = "2024-07-04/2024-06-14T14:48:51.773461/OXO_combined.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # Littlemore Community Centre, Giles Road
        if self.get_station_hash(record) in [
            "26-littlemore-community-centre",
            "25-littlemore-community-centre",
        ]:
            record = record._replace(pollingstationpostcode="OX4 4NW")

        rec = super().station_record_to_dict(record)

        # more accurate point for St Alban's Hall
        if rec["internal_council_id"] in (
            "14-st-albans-hall",
            "15-st-albans-hall",
        ):
            rec["location"] = Point(-1.232920, 51.740993, srid=4326)

        # and for Oxford Centre for Mission Studies
        if rec["internal_council_id"] in (
            "53-oxford-centre-for-mission-studies",
            "54-oxford-centre-for-mission-studies",
            "55-oxford-centre-for-mission-studies",
        ):
            rec["location"] = Point(-1.264263, 51.764185, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100121367548",  # ST. ANTONY'S COLLEGE, 62 WOODSTOCK ROAD, OXFORD
            "100121296008",  # LADY MARGARET HALL, NORHAM GARDENS, OXFORD
            "200004684441",  # STAFF COTTAGES LADY MARGARET HALL NORHAM GARDENS, OXFORD
            "10002759666",  # THE LODGE, COURT PLACE GARDENS, IFFLEY, OXFORD
            "10002759667",  # THE MANSION, COURT PLACE GARDENS, IFFLEY, OXFORD
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
