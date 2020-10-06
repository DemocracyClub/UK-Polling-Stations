"""
Data type classes used by base importers
"""

import abc
import logging
from collections import namedtuple

from django.db import connection

from addressbase.models import get_uprn_hash_table, UprnToCouncil
from uk_geo_utils.helpers import Postcode

from pollingstations.models import PollingStation


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


class CustomSet(metaclass=abc.ABCMeta):
    def __init__(self):
        self.elements = set()

    def add(self, element):
        self.elements.add(self.build_namedtuple(element))

    @abc.abstractmethod
    def build_namedtuple(self, element):
        pass


class AssignPollingStationsMixin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_polling_station_lookup(self):
        pass

    @property
    def council_id(self):  # TODO Deal with old_to_new council_ids map
        for e in self.elements:
            if isinstance(e, dict):
                return e["council"].council_id
            else:
                return e.council.council_id

    def update_uprn_to_council_model(self, polling_station_lookup=None):
        if not polling_station_lookup:
            polling_station_lookup = self.get_polling_station_lookup()

        uprns_in_council = UprnToCouncil.objects.filter(lad=self.council_id)

        for polling_station_id, uprns in polling_station_lookup.items():
            uprns_in_council.filter(uprn__in=uprns).update(
                polling_station_id=polling_station_id
            )


class DistrictSet(CustomSet, AssignPollingStationsMixin):
    NotImplemented


class StationSet(CustomSet, AssignPollingStationsMixin):
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

    def get_polling_station_lookup(self):
        NotImplemented

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


class AddressList(AssignPollingStationsMixin):
    def __init__(self, logger):
        self.elements = []
        self.logger = logger

    def append(self, address):

        if (
            not address["address"]
            or not address["postcode"]
            or not address["uprn"]
            or not address["council"]
            or not address["polling_station_id"]
        ):
            self.logger.log_message(
                logging.DEBUG,
                "Record with empty required fields found:\n%s",
                variable=address,
                pretty=True,
            )
            return

        self.elements.append(address)

    def get_uprn_lookup(self):
        # for each address, build a lookup of uprn -> set of station ids
        uprn_lookup = {}
        for record in self.elements:
            uprn = record["uprn"]
            if not uprn:
                continue
            if uprn in uprn_lookup:
                uprn_lookup[uprn].add(record["polling_station_id"])
            else:
                uprn_lookup[uprn] = {record["polling_station_id"]}

        return uprn_lookup

    # TODO be more clever to report on duplicates.
    def remove_duplicate_uprns(self):
        uprn_lookup = self.get_uprn_lookup()
        self.elements = [
            record for record in self.elements if len(uprn_lookup[record["uprn"]]) == 1
        ]

    def get_polling_station_lookup(self):
        # for each address, build a lookup of polling_station_id -> set of uprns
        polling_station_lookup = {}
        for record in self.elements:
            if record["polling_station_id"] in polling_station_lookup:
                polling_station_lookup[record["polling_station_id"]].add(record["uprn"])
            else:
                polling_station_lookup[record["polling_station_id"]] = set(
                    record["uprn"]
                )

        return polling_station_lookup

    def remove_records_not_in_addressbase(self, addressbase_data):
        self.elements = [e for e in self.elements if e["uprn"] in addressbase_data]

    def remove_records_that_dont_match_addressbase(self, addressbase_data):
        for input_record in self.elements:
            addressbase_record = addressbase_data[input_record["uprn"].lstrip("0")]

            if (
                Postcode(input_record["postcode"]).with_space
                == Postcode(addressbase_record["postcode"]).with_space
            ):
                continue
            else:
                self.elements.remove(input_record)

    def check_records(self):
        self.remove_duplicate_uprns()
        addressbase_data = get_uprn_hash_table(self.council_id)
        self.remove_records_not_in_addressbase(addressbase_data)
        self.remove_records_that_dont_match_addressbase(addressbase_data)
