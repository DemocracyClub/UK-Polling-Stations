"""
Data type classes used by base importers
"""

import abc
import logging
from collections import namedtuple
from django.db import connection
from data_collection.slugger import Slugger
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress
from uk_geo_utils.helpers import Postcode
from uk_geo_utils.models import Onspd


Station = namedtuple(
    "Station",
    [
        "council",
        "internal_council_id",
        "postcode",
        "address",
        "location",
        "polling_district_id",
    ],
)


District = namedtuple(
    "District",
    [
        "name",
        "council",
        "internal_council_id",
        "extra_id",
        "area",
        "polling_station_id",
    ],
)


class CustomSet(metaclass=abc.ABCMeta):
    def __init__(self):
        self.elements = set()

    def add(self, element):
        self.elements.add(self.build_namedtuple(element))

    @abc.abstractmethod
    def build_namedtuple(self, element):
        pass


class StationSet(CustomSet):
    def build_namedtuple(self, element):

        # Point is mutable, so we must serialize it to store in a tuple
        if "location" in element and element["location"]:
            location = element["location"].ewkb  # use ewkb so it encodes srid
        else:
            location = None

        return Station(
            element["council"],
            element["internal_council_id"],
            element.get("postcode", ""),
            element.get("address", ""),
            location,
            element.get("polling_district_id", ""),
        )

    def save(self):
        stations_db = []
        for station in self.elements:
            record = PollingStation(
                council=station.council,
                internal_council_id=station.internal_council_id,
                postcode=station.postcode,
                address=station.address,
                location=station.location,
                polling_district_id=station.polling_district_id,
            )
            stations_db.append(record)
        PollingStation.objects.bulk_create(stations_db)


class DistrictSet(CustomSet):
    def build_namedtuple(self, element):

        # MultiPolygon is mutable, so we must serialize it to store in a tuple
        area = element["area"].ewkb  # use ewkb so it encodes srid

        return District(
            element.get("name", ""),
            element["council"],
            element["internal_council_id"],
            element.get("extra_id", ""),
            area,
            element.get("polling_station_id", ""),
        )

    def save(self):
        districts_db = []
        for district in self.elements:
            record = PollingDistrict(
                name=district.name,
                council=district.council,
                internal_council_id=district.internal_council_id,
                extra_id=district.extra_id,
                area=district.area,
                polling_station_id=district.polling_station_id,
            )
            districts_db.append(record)
        PollingDistrict.objects.bulk_create(districts_db)


class AddressList:
    def __init__(self, logger):
        self.elements = []
        self.seen = set()
        self.logger = logger

    def append(self, address):

        if (
            not address["address"]
            or not address["postcode"]
            or not address["council"]
            or not address["slug"]
        ):
            self.logger.log_message(
                logging.DEBUG,
                "Record with empty required fields found:\n%s",
                variable=address,
                pretty=True,
            )
            return

        if address["slug"] not in self.seen:
            self.elements.append(address)
            self.seen.add(address["slug"])
        else:
            self.logger.log_message(
                logging.DEBUG,
                "Duplicate address found:\n%s",
                variable=address,
                pretty=True,
            )

    def get_address_lookup(self):
        # for each address, build a lookup of address -> list of station ids
        address_lookup = {}
        for record in self.elements:
            address_slug = Slugger.slugify(
                "-".join([record["address"], record["postcode"]])
            )
            record["address_slug"] = address_slug
            if address_slug in address_lookup:
                address_lookup[address_slug].add(record["polling_station_id"])
            else:
                address_lookup[address_slug] = set([record["polling_station_id"]])

        return address_lookup

    def get_uprn_lookup(self):
        # for each address, build a lookup of uprn -> list of station ids
        uprn_lookup = {}
        for record in self.elements:
            uprn = record["uprn"]
            if not uprn:
                continue
            if uprn in uprn_lookup:
                uprn_lookup[uprn].add(record["polling_station_id"])
            else:
                uprn_lookup[uprn] = set([record["polling_station_id"]])

        return uprn_lookup

    def get_ambiguous_postcodes(self, lookup, key):
        # build a set of postcodes containing
        # an address that maps to >1 polling stations
        ambiguous_postcodes = set()
        for record in self.elements:
            if not record[key]:
                continue
            if len(lookup[record[key]]) != 1:
                ambiguous_postcodes.add(record["postcode"])

        return ambiguous_postcodes

    def remove_ambiguous_addresses_by_address(self):
        address_lookup = self.get_address_lookup()
        self.remove_ambiguous_addresses(address_lookup, "address_slug")
        # cleanup
        for el in self.elements:
            el.pop("address_slug")

    def remove_ambiguous_addresses_by_uprn(self):
        """
        Note this function assumes that UPRNs and postcodes match
        this means we either need to ensure this function is called
        _after_ remove_invalid_uprns() (which is what we're doing now)
        or we'd need to switch it to index the dict on (UPRN, Postcode)
        """
        uprn_lookup = self.get_uprn_lookup()
        self.remove_ambiguous_addresses(uprn_lookup, "uprn")

    def remove_ambiguous_addresses(self, lookup, key):
        ambiguous_postcodes = self.get_ambiguous_postcodes(lookup, key)

        def keep_record(record):
            if record["postcode"] in ambiguous_postcodes:
                if record[key] and len(lookup[record[key]]) != 1:
                    # we discard it because the key itself is ambiguous
                    reason = lookup[record[key]]
                else:
                    # we've discarded it because it has the same postcode
                    # as some other addresses we have discarded
                    reason = record["postcode"]

                self.logger.log_message(
                    logging.INFO,
                    "Ambiguous addresses discarded: %s: %s",
                    variable=(record[key], reason),
                )
                return False
            return True

        if not ambiguous_postcodes:
            return

        # if we found any postcodes
        # remove all records matching any of these postcodes
        self.elements = [e for e in self.elements if keep_record(e)]

    def attach_doorstep_gridrefs(self, addressbase_data):
        for record in self.elements:
            if record["uprn"] in addressbase_data:
                record["location"] = addressbase_data[record["uprn"]]["location"]

    def remove_invalid_uprns(self, addressbase_data):
        for record in self.elements:

            # if the UPRN attached to the input record isn't present
            # in the data we fetched from AddressBase, discard the UPRN
            if record["uprn"] not in addressbase_data:
                self.logger.log_message(
                    logging.DEBUG,
                    "Removing unknown UPRN %s from record:\n%s",
                    variable=(record["uprn"], record),
                )
                record["uprn"] = ""
                continue

            # if the UPRN attached to the input record is present
            # in the data we fetched from AddressBase, but the postcode
            # on the input record doesn't match the postcode on the
            # record from AddressBase, discard the UPRN
            if record["postcode"] != addressbase_data[record["uprn"]]["postcode"]:
                self.logger.log_message(
                    logging.INFO,
                    "Removing UPRN due to postcode mismatch.\nInput Record:\n%s\nAddressbase record:\n%s",
                    variable=(record, addressbase_data[record["uprn"]]),
                )
                record["uprn"] = ""

    def get_uprns_from_addressbase(self):
        # get all the UPRNs in target local auth
        # which exist in both Addressbase and ONSUD
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                a.uprn,
                a.address,
                REPLACE(a.postcode, ' ', ''),
                a.location
            FROM addressbase_address a
            JOIN addressbase_onsud o ON a.uprn=o.uprn
            WHERE o.lad=%s;
            """,
            [self.council_id],
        )
        # return result a hash table keyed by UPRN
        return {
            row[0]: {"address": row[1], "postcode": row[2], "location": row[3]}
            for row in cursor.fetchall()
        }

    def remove_addresses_outside_target_auth(self):
        """
        Remove any addresses with a postcode which appears in our input data
        but where the postcode centroid is outside the target local auth.

        As long as we're calling this after remove_invalid_uprns()
        We can take a massive shortcut for performance here
        and only look at input records where the uprn is empty
        because by definition (see get_uprns_from_addressbase() )
        any record left with a UPRN must be inside the target local auth.

        If we've got records in the input file with a postcode centroid
        outside the target local auth this either indicates:
        a) A mistake (in which case we want to remove this bad data), or
        b) This is legit data but the postcode is split across
        multiple local authorities (in which case we just show the
        multiple_councils view, even if we hold data).

        In either case, we might as well bin the data here.
        Note if we were to get rid of the multiple_councils view
        and try to make a better job of that then we might need
        to take a more sophisticated approach here.
        """
        query_postcodes = set(
            [
                Postcode(record["postcode"]).with_space
                for record in self.elements
                if not record["uprn"]
            ]
        )
        db_postcodes = Onspd.objects.filter(pcds__in=query_postcodes, doterm="").only(
            "pcds", "oslaua"
        )
        bad_postcodes = set(
            [
                Postcode(record.pcds).without_space
                for record in db_postcodes
                if record.oslaua != self.council_id
            ]
        )

        def keep_record(record):
            if record["postcode"] in bad_postcodes:
                self.logger.log_message(
                    logging.INFO,
                    "Discarding record: Postcode centroid is outside target local authority:\n%s",
                    variable=record,
                    pretty=True,
                )
                return False
            return True

        if not bad_postcodes:
            return

        # if we found any postcodes,
        # remove all records matching any of these postcodes
        self.elements = [e for e in self.elements if keep_record(e)]

    @property
    def council_id(self):
        for e in self.elements:
            return e["council"].council_id

    def save(self, batch_size):

        self.remove_ambiguous_addresses_by_address()
        addressbase_data = self.get_uprns_from_addressbase()
        self.remove_invalid_uprns(addressbase_data)
        self.attach_doorstep_gridrefs(addressbase_data)
        self.remove_addresses_outside_target_auth()
        self.remove_ambiguous_addresses_by_uprn()

        addresses_db = []
        for address in self.elements:
            record = ResidentialAddress(
                address=address["address"],
                postcode=address["postcode"],
                polling_station_id=address["polling_station_id"],
                council=address["council"],
                slug=address["slug"],
                uprn=address["uprn"],
                location=address.get("location", None),
            )
            addresses_db.append(record)

        ResidentialAddress.objects.bulk_create(addresses_db, batch_size=batch_size)
