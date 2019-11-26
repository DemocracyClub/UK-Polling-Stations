from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E08000030"
    addresses_name = (
        "parl.2019-12-12/Version 3/polling_station_export-2019-11-14walsall.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 3/polling_station_export-2019-11-14walsall.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "100071059426":  # 193 HIGH STREET, BROWNHILLS, WALSALL
            rec["postcode"] = "WS8 6HE"

        if record.housepostcode in ["WV13 1RT", "WS9 9DE" "WS2 8AF"]:
            return None

        if record.houseid == "121600":
            return None

        if uprn in [
            "100071056617",  # WS98AW -> WS98XW : 91 GREENWOOD ROAD, ALDRIDGE, WALSALL
            "100071056618",  # WS98AW -> WS98XW : 93 GREENWOOD ROAD, ALDRIDGE, WALSALL
            "100071349914",  # WV125QB -> WV125QD : HOLLY BANK HOUSE COLTHAM ROAD, WILLENHALL, WALSALL
            "100071104119",  # WS108HW -> WS108HU : 163 WILLENHALL STREET, DARLASTON, WEDNESBURY
            "10013666599",  # WS20BA -> WS20HR : 159b CHURCHILL ROAD, BENTLEY, WALSALL
            "100071108840",  # WV125DP -> WV125DW : 74 ESSINGTON ROAD, WILLENHALL, WALSALL
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10013664416",  # WS31JR -> WS31LA : FLAT ABOVE 51 WELL LANE, BLOXWICH, WALSALL
            "100071107530",  # WV125QB -> WV125PZ : 135 COLTHAM ROAD, WILLENHALL, WALSALL
            "100071044166",  # WS99DF -> WS99DE : 370 CHESTER ROAD, STONNALL, WALSALL
            "10090063332",  # WV132AT -> WV131AT : Flat 5 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "10090063338",  # WV132AT -> WV131AT : Flat 11 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "10090063340",  # WV132AT -> WV131AT : Flat 14 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "10090063341",  # WV132AT -> WV131AT : Flat 15 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "100071371423",  # WV148ES -> WS14HE : 22 MOORCROFT, MOXLEY, WALSALL
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        rec = super().station_record_to_dict(record)

        if record.pollingstationnumber == "67":
            rec["location"] = Point(-1.971183, 52.625281, srid=4326)

        return rec
