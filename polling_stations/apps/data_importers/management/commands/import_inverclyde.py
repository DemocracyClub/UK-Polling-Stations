import re

from addressbase.models import UprnToCouncil
from data_finder.helpers import PostcodeError, geocode_point_only
from data_importers.addresshelpers import format_polling_station_address
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


def get_station_code(record):
    stationcode = getattr(record, "stationcode")
    if not stationcode:
        return ""

    stationcode = stationcode.replace("1N01", "IN01")
    stationcode = re.sub(r"[0-9]IN02", "IN02", stationcode)

    if "/" in stationcode and len(stationcode.split("/")) == 2:
        stationcode = stationcode.split("/")[0]
    return stationcode


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "IVC"
    addresses_name = "2024-07-04/2024-06-27T12:36:53.033649/districts.csv"
    stations_name = "2024-07-04/2024-06-27T12:35:55.770056/stations.csv"
    elections = ["2024-07-04"]

    def pre_import(self):
        # pass
        # We need to consider rows that don't have a uprn when importing data.

        # However there are lots of rows for other councils in this file.
        # So build a list of stations from rows that do have UPRNS
        # and then use that list of stations to make sure we check relevant rows, even if they don't have a UPRN
        council_uprns = set(
            UprnToCouncil.objects.filter(lad=self.council.geography.gss).values_list(
                "uprn", flat=True
            )
        )
        self.COUNCIL_STATIONS = set()
        data = self.get_addresses()

        for record in data:
            if record.uprn in council_uprns:
                self.COUNCIL_STATIONS.add(get_station_code(record))

    def address_record_to_dict(self, record):
        if get_station_code(record) not in self.COUNCIL_STATIONS:
            return None
        record = record._replace(stationcode=get_station_code(record))
        return super().address_record_to_dict(record)

    def get_station_point(self, record):
        if not self.allow_station_point_from_postcode:
            return None

        # otherwise, geocode using postcode
        postcode = record.postcode.strip()
        if postcode == "":
            return None

        try:
            location_data = geocode_point_only(postcode)
            location = location_data.centroid
        except PostcodeError:
            location = None

        return location

    def station_record_to_dict(self, record):
        stationcode = getattr(record, "polling_district").strip()
        if stationcode not in self.COUNCIL_STATIONS:
            return None
        address = format_polling_station_address(
            getattr(record, "polling_place").split(",")
        )
        location = self.get_station_point(record)
        return {
            "internal_council_id": stationcode,
            "postcode": getattr(record, "postcode").strip(),
            "address": address,
            "location": location,
        }
