from django.contrib.gis.geos import Point
from uk_geo_utils.helpers import Postcode
from data_collection.base_importers import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError
from data_collection.addresshelpers import (
    format_residential_address,
    format_polling_station_address,
)


class Command(BaseCsvStationsCsvAddressesImporter):
    council_id = "E07000144"
    addresses_name = "local.2019-05-02/Version 1/Broadland_poll_card_file_amended.csv"
    stations_name = "local.2019-05-02/Version 1/Broadland_poll_card_file_amended.csv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def get_station_hash(self, record):
        return "-".join([record.district.strip()])

    def get_station_address(self, record):
        return format_polling_station_address(
            [
                record.placename.strip(),
                record.placeadd1.strip(),
                record.placeadd2.strip(),
                record.placeadd3.strip(),
                record.placeadd4.strip(),
                record.placeadd5.strip(),
            ]
        )

    def get_station_point(self, record):
        postcode = record.placepcode.strip()
        if postcode == "":
            return None

        try:
            location_data = geocode_point_only(postcode)
            location = location_data.centroid
        except PostcodeError:
            location = None
        return location

    def station_record_to_dict(self, record):
        district = record.district.strip()

        # Station changes for EU election
        if district == "BC1":
            record = record._replace(placename="St Andrew and St Peter Church")
            record = record._replace(placeadd1="Church Road")
            record = record._replace(placeadd2="Blofield")
            record = record._replace(placeadd3="Norwich")
            record = record._replace(placeadd4="")
            record = record._replace(placeadd5="")
            record = record._replace(placepcode="NR13 4NA")
        if district in ["BL4", "BL5", "BL6", "BL7", "BL8", "BL9"]:
            record = record._replace(placename="The Old Rectory")
            record = record._replace(placeadd1="The Street")
            record = record._replace(placeadd2="Swannington")
            record = record._replace(placeadd3="Norwich")
            record = record._replace(placeadd4="")
            record = record._replace(placeadd5="")
            record = record._replace(placepcode="NR9 5NW")
        if district == "BY2":
            record = record._replace(placename="Rackheath Village Hall")
            record = record._replace(placeadd1="Green Lane West")
            record = record._replace(placeadd2="Rackheath")
            record = record._replace(placeadd3="Norwich")
            record = record._replace(placeadd4="")
            record = record._replace(placeadd5="")
            record = record._replace(placepcode="NR13 6LT")
        if district == "HC1":
            record = record._replace(placename="Parish Council Chamber")
            record = record._replace(placeadd1="Diamond Jubilee Lodge")
            record = record._replace(placeadd2="Wood View Road")
            record = record._replace(placeadd3="Hellesdon")
            record = record._replace(placeadd4="")
            record = record._replace(placeadd5="")
            record = record._replace(placepcode="NR6 5QB")

        location = self.get_station_point(record)

        if district == "BW1":
            location = Point(1.193280, 52.689556, srid=4326)

        return {
            "internal_council_id": district,
            "postcode": record.placepcode.strip(),
            "address": self.get_station_address(record),
            "location": location,
        }

    def address_record_to_dict(self, record):
        address = format_residential_address(
            [
                record.qualadd1.strip(),
                record.qualadd2.strip(),
                record.qualadd3.strip(),
                record.qualadd4.strip(),
                record.qualadd5.strip(),
                record.qualadd6.strip(),
            ]
        ).strip()
        postcode = Postcode(record.qualpcode.strip()).without_space
        uprn = record.qualuprn.lstrip("0").strip()

        rec = {
            "address": address,
            "postcode": postcode,
            "polling_station_id": record.district.strip(),
            "uprn": uprn,
        }

        if uprn == "100090794910":
            rec["postcode"] = "NR7 8XA"

        if uprn == "100090819705":
            rec["postcode"] = "NR7 9NQ"

        if uprn == "100090830032":
            rec["postcode"] = "NR7 9HA"

        if uprn in [
            "200004286426",  # NR134LQ -> NR134LH : SUNNY ACRES, YARMOUTH ROAD, BLOFIELD, NORWICH
            "100091546289",  # NR134BL -> NR134NH : DAVSCOTT HOUSE, 1 BUCKENHAM LANE, LINGWOOD, NORWICH
            "100090801722",  # NR70TW -> NR78UB : 35 CLOVER COURT, SPROWSTON, NORWICH
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10009922833",
            "100090814819",  # NR65NG -> NR65NS : AMBERLEA, 67 MIDDLETONS LANE, HELLESDON, NORWICH
            "10009923828",  # NR205PT -> NR205PS : 4 KERDISTON ROAD, THEMELTHORPE, DEREHAM
            "200004287047",  # NR205PT -> NR205PS : 5 KERDISTON ROAD, THEMELTHORPE, DEREHAM
        ]:
            rec["accept_suggestion"] = False

        return rec
