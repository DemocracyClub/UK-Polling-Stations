"""
Specialised base import classes for handling data exported from
popular Electoral Management Software packages
"""

import abc

from data_importers.addresshelpers import (
    format_polling_station_address,
    format_residential_address,
)
from data_importers.base_importers import (
    BaseCsvStationsCsvAddressesImporter,
    BaseStationsAddressesImporter,
)
from django.utils.text import slugify


class BaseXpressCsvImporter(BaseCsvStationsCsvAddressesImporter, metaclass=abc.ABCMeta):
    """
    Base class for processing CSVs exported from Xpress
    electoral service software
    with the addresses and stations in a single CSV file

    There are 2 formats:
    * WebLookup export (legacy format)
    * DemocracyClub export (this should be all of them these days)
    This is the parent class for both of them.
    """

    csv_delimiter = ","

    @property
    @abc.abstractmethod
    def station_postcode_field(self):
        pass

    @property
    @abc.abstractmethod
    def station_address_fields(self):
        pass

    @property
    @abc.abstractmethod
    def station_id_field(self):
        pass

    @property
    @abc.abstractmethod
    def station_easting_field(self):
        pass

    @property
    @abc.abstractmethod
    def station_northing_field(self):
        pass

    def get_station_hash(self, record):
        return "-".join([getattr(record, self.station_id_field)])

    def get_station_address(self, record):
        return format_polling_station_address(
            [getattr(record, field).strip() for field in self.station_address_fields]
        )

    def station_record_to_dict(self, record):
        address = self.get_station_address(record)
        location, location_source = self.get_station_point(record)
        return {
            "internal_council_id": getattr(record, self.station_id_field).strip(),
            "postcode": self.get_station_postcode(record),
            "address": address.strip(),
            "location": location,
            "location_source": location_source,
        }


class BaseXpressWebLookupCsvImporter(BaseXpressCsvImporter, metaclass=abc.ABCMeta):
    """
    Specialised case of BaseCsvStationsCsvAddressesImporter
    with some sensible presets for processing WebLookup
    CSVs exported from Xpress
    """

    station_postcode_field = "pollingplaceaddress7"
    station_address_fields = [
        "pollingplaceaddress1",
        "pollingplaceaddress2",
        "pollingplaceaddress3",
        "pollingplaceaddress4",
        "pollingplaceaddress5",
        "pollingplaceaddress6",
    ]
    station_id_field = "pollingplaceid"
    station_easting_field = "pollingplaceeasting"
    station_northing_field = "pollingplacenorthing"
    residential_uprn_field = "uprn"

    def address_record_to_dict(self, record):
        if record.postcode.strip() == "":
            return None

        if record.propertynumber.strip() == "0" or record.propertynumber.strip() == "":
            address = record.streetname.strip()
        else:
            address = "%s %s" % (
                record.propertynumber.strip(),
                record.streetname.strip(),
            )

        uprn = getattr(record, self.residential_uprn_field).strip()

        return {
            "address": address.strip(),
            "postcode": record.postcode.strip(),
            "polling_station_id": getattr(record, self.station_id_field).strip(),
            "uprn": uprn,
        }


class BaseXpressDemocracyClubCsvImporter(BaseXpressCsvImporter, metaclass=abc.ABCMeta):
    """
    Specialised case of BaseCsvStationsCsvAddressesImporter
    with some sensible presets for processing DemocracyClub
    CSVs exported from Xpress
    """

    station_postcode_field = "polling_place_postcode"
    station_address_fields = [
        "polling_place_name",
        "polling_place_address_1",
        "polling_place_address_2",
        "polling_place_address_3",
        "polling_place_address_4",
    ]
    station_id_field = "polling_place_id"
    station_uprn_field = "polling_place_uprn"
    station_easting_field = "polling_place_easting"
    station_northing_field = "polling_place_northing"
    residential_uprn_field = "property_urn"

    def address_record_to_dict(self, record):
        if record.addressline6.strip() == "":
            return None

        address = format_residential_address(
            [
                record.addressline1,
                record.addressline2,
                record.addressline3,
                record.addressline4,
                record.addressline5,
            ]
        )

        uprn = getattr(record, self.residential_uprn_field).strip()

        return {
            "address": address.strip(),
            "postcode": record.addressline6.strip(),
            "polling_station_id": getattr(record, self.station_id_field).strip(),
            "uprn": uprn,
        }


class BaseXpressDCCsvInconsistentPostcodesImporter(
    BaseXpressDemocracyClubCsvImporter, metaclass=abc.ABCMeta
):
    """
    Sometimes the postcode doesn't appear in a consistent
    column and we need to work around that
    """

    # concat all the address columns together into address
    # don't bother trying to split into address/postcode
    station_address_fields = [
        "polling_place_name",
        "polling_place_address_1",
        "polling_place_address_2",
        "polling_place_address_3",
        "polling_place_address_4",
        "polling_place_postcode",
    ]
    station_postcode_search_fields = [
        "polling_place_postcode",
        "polling_place_address_4",
        "polling_place_address_3",
    ]

    def station_record_to_dict(self, record):
        address = self.get_station_address(record)
        location, location_source = self.get_station_point(record)
        return {
            "internal_council_id": getattr(record, self.station_id_field).strip(),
            "postcode": "",  # don't rely on get_station_postcode()
            "address": address.strip(),
            "location": location,
            "location_source": location_source,
        }

    def get_station_postcode(self, record):
        # postcode does not appear in a consistent column
        # return the contents of the last populated address
        # field and we'll attempt to geocode with that
        for field in self.station_postcode_search_fields:
            if getattr(record, field):
                return getattr(record, field).strip()
        return None


class BaseHalaroseCsvImporter(
    BaseCsvStationsCsvAddressesImporter, metaclass=abc.ABCMeta
):
    """
    Base class for processing data exported from Idox Eros
    with the addresses and stations in a single CSV file
    This software used to be called Halarose, hence the name

    This is a specialised case of BaseCsvStationsCsvAddressesImporter
    with some sensible presets for processing CSVs in this format
    but we can override them if necessary
    """

    csv_delimiter = ","
    station_easting_field = "pollingvenueeasting"
    station_northing_field = "pollingvenuenorthing"
    station_postcode_field = "pollingstationpostcode"
    station_uprn_field = "pollingvenueuprn"
    station_id_field = "pollingvenueid"
    station_address_fields = [
        "pollingstationname",
        "pollingstationaddress1",
        "pollingstationaddress2",
        "pollingstationaddress3",
        "pollingstationaddress4",
        "pollingstationaddress5",
    ]
    residential_uprn_field = "uprn"

    def get_station_hash(self, record):
        return "-".join(
            [
                record.pollingstationnumber.strip(),
                slugify(record.pollingstationname.strip())[:90],
            ]
        )

    def get_station_address(self, record):
        return format_polling_station_address(
            [
                getattr(record, field).strip()
                for field in self.station_address_fields
                if getattr(record, field).strip()
            ]
        )

    def station_record_to_dict(self, record):
        if record.pollingstationnumber.strip() == "n/a":
            return None

        address = self.get_station_address(record)
        location, location_source = self.get_station_point(record)
        return {
            "internal_council_id": self.get_station_hash(record),
            "postcode": getattr(record, self.station_postcode_field).strip(),
            "address": address.strip(),
            "location": location,
            "location_source": location_source,
        }

    def get_residential_address(self, record):
        def replace_na(text):
            if text.strip() == "n/a":
                return ""
            return text.strip()

        address_line_1 = replace_na(record.housename)
        if replace_na(record.substreetname):
            address_line_2 = (
                replace_na(record.housenumber) + " " + replace_na(record.substreetname)
            ).strip()
            address_line_3 = (
                replace_na(record.streetnumber) + " " + replace_na(record.streetname)
            ).strip()
        else:
            address_line_2 = (
                replace_na(record.housenumber) + " " + replace_na(record.streetname)
            ).strip()
            address_line_3 = ""

        address = format_residential_address(
            [
                address_line_1.strip(),
                address_line_2.strip(),
                address_line_3.strip(),
                replace_na(record.locality),
                replace_na(record.town),
                replace_na(record.adminarea),
            ]
        )

        return address.strip()

    def address_record_to_dict(self, record):
        if record.postcode.strip() == "":
            return None

        address = format_residential_address(
            [
                record.addressline1,
                record.addressline2,
                record.addressline3,
                record.addressline4,
                record.addressline5,
            ]
        )

        if record.pollingstationnumber.strip() == "n/a":
            station_id = ""
        else:
            station_id = self.get_station_hash(record)

        uprn = getattr(record, self.residential_uprn_field).strip()

        return {
            "address": address,
            "postcode": record.postcode.strip(),
            "polling_station_id": station_id,
            "uprn": uprn,
        }


class BaseDemocracyCountsCsvImporter(
    BaseCsvStationsCsvAddressesImporter, metaclass=abc.ABCMeta
):
    """
    Base class for processing data exported from Democracy Counts
    electoral service software: http://www.democracycounts.co.uk/
    with the addresses and stations in a single CSV file

    This is a specialised case of BaseCsvStationsCsvAddressesImporter
    with some sensible presets for processing CSVs in this format
    but we can override them if necessary
    """

    csv_delimiter = ","
    station_name_field = "placename"
    address_fields = ["add1", "add2", "add3", "add4", "add5", "add6"]
    postcode_field = "postcode"
    station_id_field = "stationcode"
    station_postcode_field = "postcode"
    station_easting_field = "xordinate"
    station_northing_field = "yordinate"

    residential_uprn_field = "uprn"

    def address_record_to_dict(self, record):
        if getattr(record, self.postcode_field).strip() == "A1 1AA":
            # this is a dummy record
            return None

        if not getattr(record, self.postcode_field).strip():
            return None

        address = format_residential_address(
            [getattr(record, field) for field in self.address_fields]
        )

        if "Dummy Record" in address:
            return None

        uprn = getattr(record, self.residential_uprn_field).strip()

        return {
            "address": address,
            "postcode": getattr(record, self.postcode_field).strip(),
            "polling_station_id": getattr(record, self.station_id_field).strip(),
            "uprn": uprn,
        }

    def get_station_address(self, record):
        return format_polling_station_address(
            [getattr(record, self.station_name_field)]
            + [getattr(record, field) for field in self.address_fields]
        )

    def station_record_to_dict(self, record):
        address = self.get_station_address(record)
        location, location_source = self.get_station_point(record)

        return {
            "internal_council_id": getattr(record, self.station_id_field).strip(),
            "postcode": getattr(record, self.postcode_field).strip(),
            "address": address,
            "location": location,
            "location_source": location_source,
        }


class BaseFcsDemocracyClubImporter(
    BaseStationsAddressesImporter, metaclass=abc.ABCMeta
):
    """
    Base class for processing data exported from FCS ElectionsPro
    electoral service software: https://fcssoftware.co.uk/fcs-elections
    with the addresses and stations in a single CSV file

    This class assumes that we're going to take a snapshot of data from the
    /api/DemocracyClub/Election/{election_id}/PollingStation
    endpoint, save it to a JSON file, and then import it from there.
    """

    srid = 4326
    addresses_filetype = "json"
    stations_filetype = "json"
    station_name_field = "name"
    address_fields = [
        "addressLine1",
        "addressLine2",
        "addressLine3",
        "addressLine4",
        "addressLine5",
    ]
    postcode_field = "addressPostCode"
    station_id_field = "id"
    residential_uprn_field = "addressUprn"

    def get_addresses(self):
        stations = super().get_addresses()
        addresses = []
        for station in stations:
            for prop in station["properties"]:
                prop[self.station_id_field] = station[self.station_id_field]
            addresses += station["properties"]
        return addresses

    def address_record_to_dict(self, record):
        if not record.get(self.postcode_field).strip():
            return None

        address = format_residential_address(
            [record.get(field) for field in self.address_fields]
        )

        uprn = str(record.get(self.residential_uprn_field))

        return {
            "address": address,
            "postcode": record.get(self.postcode_field).strip(),
            "polling_station_id": str(record.get(self.station_id_field)),
            "uprn": uprn,
        }

    def get_station_id(self, record):
        return record.get(self.station_id_field)

    def get_station_postcode(self, record):
        return record.get(self.postcode_field).strip()

    def get_station_coordinates(self, record):
        return record["longitude"], record["latitude"]

    def station_record_to_dict(self, record):
        address = format_polling_station_address(
            [record.get(self.station_name_field)]
            + [record.get(field) for field in self.address_fields]
        )

        location, location_source = self.get_station_point(record)

        return {
            "internal_council_id": self.get_station_id(record),
            "postcode": self.get_station_postcode(record),
            "address": address,
            "location": location,
            "location_source": location_source,
        }
