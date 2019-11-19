from django.contrib.gis.geos import Point
from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError
from data_collection.addresshelpers import (
    format_residential_address,
    format_polling_station_address,
)


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id = "E08000022"
    addresses_name = "parl.2019-12-12/Version 1/Find My Polling Station.csv"
    stations_name = "parl.2019-12-12/Version 1/Find My Polling Station.csv"
    elections = ["parl.2019-12-12"]

    def get_station_hash(self, record):
        return "-".join([record.col12.strip()])

    def get_station_address(self, record):
        return format_polling_station_address(
            [
                record.col37.strip(),
                record.col38.strip(),
                record.col39.strip(),
                record.col40.strip(),
                record.col41.strip(),
            ]
        )

    def get_station_point(self, record):
        postcode = record.col46.strip()
        if postcode == "":
            return None

        try:
            location_data = geocode_point_only(postcode)
            location = location_data.centroid
        except PostcodeError:
            location = None
        return location

    def station_record_to_dict(self, record):
        location = self.get_station_point(record)
        code = record.col12.strip()
        postcode = record.col46.strip()

        if code == "OE":
            postcode = "NE30 4RH"
            location = Point(-1.429405, 55.019131, srid=4326)

        if code == "ME":
            location = Point(-1.457842, 55.025205, srid=4326)

        return {
            "internal_council_id": code,
            "postcode": postcode,
            "address": self.get_station_address(record),
            "location": location,
        }

    def address_record_to_dict(self, record):
        uprn = record.col36.strip()
        postcode = record.col35.strip()

        if uprn == "47237285":
            return None

        if postcode in ["NE25 9BE", "NE27 0PJ"]:
            return None

        address = format_residential_address(
            [
                record.col27.strip(),
                record.col28.strip(),
                record.col29.strip(),
                record.col30.strip(),
                record.col31.strip(),
                record.col32.strip(),
            ]
        )
        rec = {
            "address": address.strip(),
            "postcode": postcode,
            "polling_station_id": record.col12.strip(),
            "uprn": uprn,
        }

        if address == "30 PHOENIX RISE, MOOR PARK NORTH SHIELDS":
            return None

        if uprn in [
            "47029975",  # NE237JT -> NE237JU : EAST BARNS, GREENS HOUSES FARM, DUDLEY LANE, SEATON BURN
            "47035320",  # NE237AG -> NE237AF : RESIDENTIAL HOUSE AT, 83 FERN DRIVE, DUDLEY
            "47093421",  # NE299JU -> NE296SL : THE OLD VICARAGE, PRESTON ROAD, NORTH SHIELDS
            "47102033",  # NE304HQ -> NE304NU : FLAT 3, 45 PERCY GARDENS, TYNEMOUTH
            "47102032",  # NE304HQ -> NE304NU : FLAT 2, 45 PERCY GARDENS, TYNEMOUTH
            "47072823",  # NE258RU -> NE270XL : 19 PRIORY AVENUE, WHITLEY BAY
            "47072822",  # NE258RU -> NE270XL : 18 PRIORY AVENUE, WHITLEY BAY
            "47072818",  # NE258RU -> NE270XL : 14 PRIORY AVENUE, WHITLEY BAY
        ]:
            rec["accept_suggestion"] = False

        return rec
