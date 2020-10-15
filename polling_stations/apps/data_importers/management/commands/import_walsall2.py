from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "E08000030"
    addresses_name = (
        "2020-02-03T14:09:25.972119/polling_station_export-2020-02-03Walsall.csv"
    )
    stations_name = (
        "2020-02-03T14:09:25.972119/polling_station_export-2020-02-03Walsall.csv"
    )
    elections = ["2020-05-07"]

    # def address_record_to_dict(self, record):
    #     rec = super().address_record_to_dict(record)
    #     uprn = record.uprn.strip().lstrip("0")
    #
    #     if uprn in [
    #         "100071345467",  # PEARTREE FARM, FISHLEY LANE, appears twice two different addresses.
    #         "10090903310",  # Flat 1, 73 STAFFORD STREET, WALSALL
    #     ]:
    #         return None
    #
    #     if record.houseid == "121600":  # '12 FORGE LANE, ALDRIDGE, WALSALL'
    #         return None
    #
    #     if record.housepostcode in [
    #         "WV12 5YH",
    #         "WS10 7TG",
    #         "WS2 8AF",
    #         "WS9 9DE",
    #         "WS2 8AF",
    #     ]:
    #         return None
    #
    #     if uprn in [
    #         "100071056617",  # WS98AW -> WS98XW : 91 GREENWOOD ROAD, ALDRIDGE, WALSALL
    #         "100071056618",  # WS98AW -> WS98XW : 93 GREENWOOD ROAD, ALDRIDGE, WALSALL
    #         "100071349914",  # WV125QB -> WV125QD : HOLLY BANK HOUSE COLTHAM ROAD, WILLENHALL, WALSALL
    #         "100071104119",  # WS108HW -> WS108HU : 163 WILLENHALL STREET, DARLASTON, WEDNESBURY
    #         "10013666599",  # WS20BA -> WS20HR : 159b CHURCHILL ROAD, BENTLEY, WALSALL
    #         "100071108840",  # WV125DP -> WV125DW : 74 ESSINGTON ROAD, WILLENHALL, WALSALL
    #     ]:
    #         rec["accept_suggestion"] = True
    #
    #     if uprn in [
    #         "10013664416",  # WS31JR -> WS31LA : FLAT ABOVE 51 WELL LANE, BLOXWICH, WALSALL
    #         "100071107530",  # WV125QB -> WV125PZ : 135 COLTHAM ROAD, WILLENHALL, WALSALL
    #         "100071044166",  # WS99DF -> WS99DE : 370 CHESTER ROAD, STONNALL, WALSALL
    #         "100071371423",  # WV148ES -> WS14HE : 22 MOORCROFT, MOXLEY, WALSALL
    #     ]:
    #         rec["accept_suggestion"] = False
    #
    #     return rec

    def station_record_to_dict(self, record):

        rec = super().station_record_to_dict(record)

        # 66-st-michaels-church
        if record.pollingstationnumber == "66":
            rec["location"] = Point(-1.971183, 52.625281, srid=4326)

        return rec
