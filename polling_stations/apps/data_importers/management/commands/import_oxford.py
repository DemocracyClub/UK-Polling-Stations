from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "OXO"
    addresses_name = "2024-05-02/2024-03-28T11:08:13.289353/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-28T11:08:13.289353/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # Littlemore Community Centre, Giles Road
        if record.pollingstationnumber == "49":
            record = record._replace(pollingstationpostcode="OX4 4NW")

        rec = super().station_record_to_dict(record)

        # more accurate point for St Alban's Hall
        if rec["internal_council_id"] in (
            "40-st-albans-hall",
            "41-st-albans-hall",
        ):
            rec["location"] = Point(-1.232920, 51.740993, srid=4326)

        # and for Oxford Centre for Mission Studies
        if rec["internal_council_id"] in (
            "14-oxford-centre-for-mission-studies",
            "15-oxford-centre-for-mission-studies",
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
