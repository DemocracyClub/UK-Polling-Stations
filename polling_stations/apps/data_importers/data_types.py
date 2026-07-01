"""
Data type classes used by base importers
"""

import abc
import logging
from collections import namedtuple


from addressbase.models import Address, UprnToCouncil, get_uprn_hash_table
from councils.models import Council
from pollingstations.models import PollingStation
from uk_geo_utils.helpers import Postcode

Station = namedtuple(
    "Station",
    [
        "council",
        "internal_council_id",
        "postcode",
        "address",
        "location",
        "location_source",
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


class RecordsNotSavedException(Exception):
    """Records weren't saved to the db"""

    pass


class CustomSet(metaclass=abc.ABCMeta):
    def __init__(self):
        self.elements = set()
        self.saved = False

    def add(self, element):
        self.elements.add(self.build_namedtuple(element))
        self.saved = False

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
            return e.council.council_id
        return None

    @property
    def gss_code(self):
        return Council.objects.get(pk=self.council_id).geography.gss

    def update_uprn_to_council_model(self, polling_station_lookup=None):
        if not polling_station_lookup:
            polling_station_lookup = self.get_polling_station_lookup()

        uprns_in_council = UprnToCouncil.objects.filter(lad=self.gss_code)
        for polling_station_id, uprns in polling_station_lookup.items():
            uprns_in_council.filter(uprn__in=uprns).update(
                polling_station_id=polling_station_id
            )


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
            element.get("location_source", ""),
            element.get("polling_district_id", ""),
        )

    @property
    def council_id(self):  # TODO Deal with old_to_new council_ids map
        for e in self.elements:
            if isinstance(e, dict):
                return e["council"].council_id
            return e.council.council_id
        return None

    def save(self):
        stations_db = []
        for station in self.elements:
            record = PollingStation(
                council=station.council,
                internal_council_id=station.internal_council_id,
                postcode=station.postcode,
                address=station.address,
                location=station.location,
                location_source=station.location_source,
                polling_district_id=station.polling_district_id,
            )
            stations_db.append(record)
        PollingStation.objects.bulk_create(stations_db)
        self.saved = True


class AddressList(AssignPollingStationsMixin):
    def __init__(self, logger):
        self.elements = []
        self.logger = logger

    def append(self, address):
        if (
            not address["address"]
            or not address["postcode"]
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

    def get_council_split_postcodes(self):
        postcode_lookup = {}
        for record in self.elements:
            postcode = record["postcode"]
            if postcode in postcode_lookup:
                postcode_lookup[postcode].add(record["polling_station_id"])
            else:
                postcode_lookup[postcode] = {record["polling_station_id"]}
        return [k for k, v in postcode_lookup.items() if len(v) > 1]

    def remove_non_numeric_uprns(self):
        bad_uprn_records = [e for e in self.elements if not e["uprn"].strip().isdigit()]
        if bad_uprn_records:
            self.logger.log_message(
                logging.WARNING,
                f"{len(bad_uprn_records)} addresses have non-numeric UPRNs in council data. These have been discarded.",
            )
            for record in bad_uprn_records:
                self.logger.log_message(
                    logging.INFO,
                    f'"NON_NUMERIC_UPRN","{record.get("uprn")}","{record.get("address")}","{record.get("postcode")}"',
                )
        self.elements = [e for e in self.elements if e["uprn"].isdigit()]

    def remove_duplicate_uprns(self):
        uprn_lookup = self.get_uprn_lookup()
        duplicate_uprns = {
            uprn: stations
            for uprn, stations in uprn_lookup.items()
            if len(stations) > 1
        }
        if duplicate_uprns:
            duplicate_address_count = sum(
                1 for e in self.elements if e["uprn"] in duplicate_uprns
            )
            self.logger.log_message(
                logging.WARNING,
                f"{duplicate_address_count} UPRNs are assigned to more than one station in council data. These have been discarded.",
            )
            for uprn, stations in sorted(duplicate_uprns.items()):
                self.logger.log_message(
                    logging.INFO,
                    f'"UPRN_ASSIGNED_MULTIPLE_STATIONS","{uprn}","{stations}"',
                )

        self.elements = [
            record for record in self.elements if record["uprn"] not in duplicate_uprns
        ]

    def get_polling_station_lookup(self):
        # for each address, build a lookup of polling_station_id -> set of uprns
        polling_station_lookup = {}
        for record in self.elements:
            if record["polling_station_id"] in polling_station_lookup:
                polling_station_lookup[record["polling_station_id"]].add(record["uprn"])
            else:
                polling_station_lookup[record["polling_station_id"]] = {record["uprn"]}

        return polling_station_lookup

    def remove_records_not_in_addressbase(self, addressbase_data):
        not_in_addressbase = [
            e for e in self.elements if e["uprn"] not in addressbase_data
        ]
        if not_in_addressbase:
            self.logger.log_message(
                logging.WARNING,
                f"{len(not_in_addressbase)} UPRNs from council data not found in addressbase. These have been discarded.",
            )
            for record in not_in_addressbase:
                self.logger.log_message(
                    logging.INFO,
                    f'"UPRN_MISSING_IN_ADDRESSBASE","{record.get("uprn")}", "{record.get("address")}", "{record.get("postcode")}"',
                )

        self.elements = [e for e in self.elements if e["uprn"] in addressbase_data]

    def remove_records_that_dont_match_addressbase(self, addressbase_data):
        to_remove = []
        for input_record in self.elements:
            addressbase_record = addressbase_data[input_record["uprn"].lstrip("0")]

            if (
                Postcode(input_record["postcode"]).with_space
                == Postcode(addressbase_record["postcode"]).with_space
            ):
                continue

            to_remove.append(input_record)
        if len(to_remove) >= 1:
            self.logger.log_message(
                logging.WARNING,
                f"{len(to_remove)} council records UPRNs found in addressbase but postcodes don't match. These have been discarded.",
            )
            for record in to_remove:
                self.logger.log_message(
                    logging.INFO,
                    f'"POSTCODE_DIFFERS","{record.get("uprn")}", "{record.get("address")}", "{record.get("postcode")}"',
                )
        self.elements = [e for e in self.elements if e not in to_remove]

    def remove_records_missing_uprns(self):
        missing_uprn_records = [e for e in self.elements if not e.get("uprn")]
        if missing_uprn_records:
            self.logger.log_message(
                logging.WARNING,
                f"{len(missing_uprn_records)} Addresses are missing a UPRN in council data. These have been discarded",
            )
            for record in missing_uprn_records:
                self.logger.log_message(
                    logging.INFO,
                    f'"UPRN_MISSING_IN_COUNCIL_DATA","{record.get("address")}", "{record.get("postcode")}"',
                )

        self.elements = [e for e in self.elements if e.get("uprn", None)]

    def check_split_postcodes_are_split(self, split_postcodes):
        postcodes_to_warn = []
        for postcode in split_postcodes:
            addresslist_records = [
                e for e in self.elements if e["postcode"] == postcode
            ]
            if len({r["polling_station_id"] for r in addresslist_records}) > 1:
                continue
            db_records = Address.objects.filter(postcode=postcode)
            if len(db_records) > len(addresslist_records):
                continue

            postcodes_to_warn.append('"' + postcode + '"')
        if postcodes_to_warn:
            self.logger.log_message(
                logging.WARNING,
                f"These postcodes are split in council data: {', '.join(sorted(postcodes_to_warn))}, "
                "but won't be in the db once imported.",
                pretty=True,
            )

    def check_records(self):
        split_postcodes = self.get_council_split_postcodes()
        self.remove_records_missing_uprns()
        self.remove_non_numeric_uprns()
        self.remove_duplicate_uprns()
        addressbase_data = get_uprn_hash_table(self.gss_code)
        self.remove_records_not_in_addressbase(addressbase_data)
        self.remove_records_that_dont_match_addressbase(addressbase_data)
        self.check_split_postcodes_are_split(split_postcodes)
