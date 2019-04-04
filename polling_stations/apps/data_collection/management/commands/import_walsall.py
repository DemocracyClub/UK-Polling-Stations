from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E08000030"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-25walsall.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-25walsall.csv"
    )
    elections = ["local.2019-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "100071059426":
            rec["postcode"] = "WS8 6HE"
        if uprn == "10093459127":
            rec["postcode"] = "WS4 1JQ"

        if record.housepostcode == "WV13 1RT":
            return None

        if record.housepostcode == "WS9 9DE":
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
            "100071106025",  # WV131AX -> WV131AB : LIVING AREA 10/12 BLOXWICH ROAD SOUTH, WILLENHALL, WALSALL
            "10090902647",  # WV132AB -> WV132QF : Flat 13 42 BILSTON LANE, WILLENHALL, WALSALL
            "10090063332",  # WV132AT -> WV131AT : Flat 5 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "10090063335",  # WV132AT -> WV131AT : Flat 8 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "10090063338",  # WV132AT -> WV131AT : Flat 11 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "10090063340",  # WV132AT -> WV131AT : Flat 14 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "10090063341",  # WV132AT -> WV131AT : Flat 15 WATERGLADES, ROSE HILL, WILLENHALL, WALSALL
            "100071072656",  # WS86AT -> WS90JN : FLAT 1B NEW ROAD, BROWNHILLS, WALSALL
            "100071371423",  # WV148ES -> WS14HE : 22 MOORCROFT, MOXLEY, WALSALL
            "200003319588",  # WV125BY -> WS13PP : 21 SQUIRES GROVE, WILLENHALL, WALSALL
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "40":
            record = record._replace(pollingstationpostcode="WV13 1QG")

        if record.pollingstationnumber == "10":
            record = record._replace(pollingstationaddress_1="50 RYECROFT PLACE")

        rec = super().station_record_to_dict(record)

        if record.pollingstationnumber == "68":
            rec["location"] = Point(-1.971183, 52.625281, srid=4326)

        return rec
