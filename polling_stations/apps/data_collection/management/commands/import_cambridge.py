from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000008"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-15cam.csv"
    )
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-15cam.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "17-st-philip-howard-church-centre":
            rec["location"] = Point(0.16067, 52.18589, srid=4326)

        if rec["internal_council_id"] == "38-the-c3-centre":
            rec["location"] = Point(0.1572, 52.2003, srid=4326)

        # user issue report #105
        if rec["internal_council_id"] == "31-trinity-old-field-pavilion":
            rec["location"] = Point(0.106029, 52.207284, srid=4326)

        # user issue report #129
        if rec["internal_council_id"] == "2-east-barnwell-community-centre":
            rec["location"] = Point(0.165576, 52.212132, srid=4326)

        # report from council
        if rec["internal_council_id"] == "13-seminar-rooms-3-4-churchill-college":
            rec["location"] = Point(0.099002518, 52.215464, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in [
            "CB5 8JJ",
            "CB5 8HL",
        ]:
            return None

        if uprn in [
            "200004210782",  # CB30DP -> CB30DS : 40A STOREY'S WAY, CAMBRIDGE
            "200004210783",  # CB30DP -> CB30DS : 40B STOREY'S WAY, CAMBRIDGE
            "200004210784",  # CB30DP -> CB30DS : 40C STOREY'S WAY, CAMBRIDGE
            "10090970400",  # CB11BN -> CB18BN : 22 BROTHERS' PLACE, CAMBRIDGE
            "10090628073",  # CB29BE -> CB29BA : THE CHERRY BUILDING, 119 ADDENBROOKE'S ROAD, TRUMPINGTON, CAMBRIDGE
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200004159235",  # CB30DJ -> CB30UD : 1 GRAVEL HILL COTTAGES, HUNTINGDON ROAD, CAMBRIDGE
            "200004159236",  # CB30DJ -> CB30UD : 2 GRAVEL HILL COTTAGES, HUNTINGDON ROAD, CAMBRIDGE
            "10002562588",  # CB21TQ -> CB21TP : THE MASTER'S LODGE, TRINITY COLLEGE, CAMBRIDGE
            "10091728051",  # CB41HA -> CB41ZA : HOUSEBOAT POLARIS, M1008 RIVER CAM, CAMBRIDGE
            "10023619475",  # CB39JN -> CB29LH : 101A GRANTCHESTER MEADOWS, CAMBRIDGE
            "10002562986",  # CB58PE -> CB58SP : CEMETERY LODGE , CITY CEMETERY, NEWMARKET ROAD, CAMBRIDGE
            "200004203530",  # CB30DZ -> CB30DQ : WYCHFIELD LODGE, HUNTINGDON ROAD, CAMBRIDGE
            "200004203528",  # CB30DZ -> CB30DQ : WALTER CHRISTIE HOUSE, HUNTINGDON ROAD, CAMBRIDGE
            "200004209699",  # CB30DZ -> CB30DQ : LAUNCELOT FLEMING HOUSE, HUNTINGDON ROAD, CAMBRIDGE
        ]:
            rec["accept_suggestion"] = False

        return rec
