"""
Import Redbridge

note: this script takes quite a long time to run
"""
from data_importers.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError


class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Redbridge Council
    """

    council_id = "E09000026"
    addresses_name = (
        "rev01-2016/LLPG Addresses - Polling Station Finder - EU referendum.csv"
    )
    stations_name = "rev01-2016/Polling Stations - EU referendum.csv"
    elections = ["ref.2016-06-23"]

    def station_record_to_dict(self, record):

        # no points supplied, so attempt to attach them by geocoding
        if record.postcode:
            try:
                location_data = geocode_point_only(record.postcode)
                location = location_data.centroid
            except PostcodeError:
                location = None
        else:
            location = None

        return {
            "internal_council_id": record.district_code.strip(),
            "postcode": record.postcode.strip(),
            "address": record.address.strip(),
            "location": location,
        }

    def address_record_to_dict(self, record):

        address_parts = record.postal_address.strip().split(", ")
        postcode = address_parts[-1]  # every address has a postcode :D
        address = ", ".join(address_parts[:-1])

        # There are 6 addresses which don't
        # map to any station - exclude them
        if not record.district_code:
            return None

        # 20 exact dupes will be discarded
        return {
            "address": address,
            "postcode": postcode,
            "polling_station_id": record.district_code.strip(),
        }
