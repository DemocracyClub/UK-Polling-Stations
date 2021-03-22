from uk_geo_utils.helpers import Postcode
from data_importers.base_importers import BaseCsvStationsCsvAddressesImporter
from data_importers.addresshelpers import (
    format_residential_address,
    format_polling_station_address,
)
from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = "2021-03-05T09:13:07.744121/Broadland Democracy Club - Polling Districts- Election ID 5 County Council.csv"
    stations_name = "2021-03-05T09:13:07.744121/Broadland Democracy Club - Polling Stations- Election ID 5 County Council.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.placename == "SPROWSTON W CRICKET CLUB":
            record = record._replace(placename="SPROWSTON CRICKET CLUB")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in ["NR13 3BH"]:  # split
            return None

        if record.postcode in ["NR10 4DA"]:
            # coincident with another property at different polling place; wide postcode
            return None

        uprn = record.uprn.lstrip("0").strip()

        if uprn == "200004453970":
            # errant; multiple addresses, so they'll be told to check
            return None

        if uprn == "100090794910":
            record = record._replace(postcode="NR7 8XA")

        return super().address_record_to_dict(record)
