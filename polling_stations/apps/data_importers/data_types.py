"""
Data type classes used by base importers
"""

import abc
import logging
from collections import namedtuple

from addressbase.models import Address, UprnToCouncil, get_uprn_hash_table
from councils.models import Council, CouncilGeography
from django.db import connection
from pollingstations.models import PollingDistrict, PollingStation
from uk_geo_utils.helpers import Postcode

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

    @abc.abstractmethod
    def update_uprn_to_council_model(self, polling_station_lookup=None):
        pass


class DistrictSet(CustomSet, AssignPollingStationsMixin):
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
        self.saved = True

    def get_uprns_by_district(self):
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT a.uprn, d.polling_station_id
                FROM addressbase_address a
                    JOIN addressbase_uprntocouncil u
                    ON a.uprn = u.uprn
                    JOIN pollingstations_pollingdistrict d
                    ON ST_Contains(d.area, a.location)
                WHERE d.council_id=%s
                AND u.lad=%s
            """,
            [self.council_id, self.gss_code],
        )
        return cursor.fetchall()

    def get_uprns_by_district_join_stations(self):
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT a.uprn, s.internal_council_id
                FROM addressbase_address a
                    JOIN addressbase_uprntocouncil u
                    ON a.uprn = u.uprn
                    JOIN pollingstations_pollingdistrict d
                    ON ST_Contains(d.area, a.location)
                    JOIN pollingstations_pollingstation s
                    ON s.polling_district_id = d.internal_council_id
                WHERE d.council_id=%s
                AND u.lad=%s
                AND s.council_id=%s
            """,
            [self.council_id, self.gss_code, self.council_id],
        )
        return cursor.fetchall()

    def get_polling_station_lookup(self, districts_have_station_ids=True):
        """
        for each address, build a lookup of polling_station_id -> set of uprns
        """
        if not self.saved:
            raise RecordsNotSavedException(
                "You must have called self.save() before self.get_polling_station_lookup()"
            )

        polling_station_lookup = {}

        if districts_have_station_ids:
            uprns = self.get_uprns_by_district()
        else:
            uprns = self.get_uprns_by_district_join_stations()

        for row in uprns:
            uprn = row[0]
            polling_station_id = row[1]
            if polling_station_id not in polling_station_lookup:
                polling_station_lookup[polling_station_id] = {uprn}
            else:
                polling_station_lookup[polling_station_id].add(uprn)

        return polling_station_lookup

    def update_uprn_to_council_model(
        self, districts_have_station_ids=True, polling_station_lookup=None
    ):
        if not polling_station_lookup:
            polling_station_lookup = self.get_polling_station_lookup(
                districts_have_station_ids
            )

        uprns_in_council = UprnToCouncil.objects.filter(lad=self.gss_code)
        seen = set()
        for polling_station_id, uprns in polling_station_lookup.items():
            uprns_in_council.filter(uprn__in=uprns).update(
                polling_station_id=polling_station_id
            )

            # We have to do this in case there are two districts which overlap
            # and an address falls within that overlapping area.
            duplicates = [u for u in uprns if u in seen]
            uprns_in_council.filter(uprn__in=duplicates).update(polling_station_id="")
            seen.update(uprns)


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
                polling_district_id=station.polling_district_id,
            )
            stations_db.append(record)
        PollingStation.objects.bulk_create(stations_db)
        self.saved = True


class AddressList(AssignPollingStationsMixin):
    def __init__(self, logger, extra_councils=None):
        if extra_councils is None:
            extra_councils = []

        self.elements = []
        self.logger = logger
        self.extra_councils = extra_councils

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

    @property
    def council_ids(self) -> list[str]:  # TODO Deal with old_to_new council_ids map
        return [self.council_id] + self.extra_councils

    @property
    def gss_codes(self) -> list[str]:
        return CouncilGeography.objects.filter(
            council_id__in=self.council_ids
        ).values_list("gss", flat=True)

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

    # TODO be more clever to report on duplicates.
    def remove_duplicate_uprns(self):
        uprn_lookup = self.get_uprn_lookup()

        duplicate_count = len(
            [e for e in self.elements if len(uprn_lookup[e["uprn"]]) > 1]
        )
        if duplicate_count >= 1:
            self.logger.log_message(
                logging.WARNING,
                f"{duplicate_count} UPRNs are assigned to more than one station in council data. These have been discarded.",
            )

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
                polling_station_lookup[record["polling_station_id"]] = {record["uprn"]}

        return polling_station_lookup

    def remove_records_not_in_addressbase(self, addressbase_data):
        not_in_address_base_count = len(
            [e for e in self.elements if e["uprn"] not in addressbase_data]
        )
        if not_in_address_base_count >= 1:
            self.logger.log_message(
                logging.WARNING,
                f"{not_in_address_base_count} UPRNs from council data not found in addressbase. These have been discarded.",
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
        self.elements = [e for e in self.elements if e not in to_remove]

    def remove_records_missing_uprns(self):
        uprn_missing_count = len([e for e in self.elements if not e.get("uprn")])
        if uprn_missing_count >= 1:
            self.logger.log_message(
                logging.WARNING,
                f"{uprn_missing_count} Addresses are missing a UPRN in council data. These have been discarded",
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
                f"These postcodes are split in council data: {', '.join(postcodes_to_warn)}, "
                "but won't be in the db once imported.",
                pretty=True,
            )

    def update_uprn_to_council_model(self, polling_station_lookup=None):
        if not polling_station_lookup:
            polling_station_lookup = self.get_polling_station_lookup()

        uprns_in_council = UprnToCouncil.objects.filter(lad__in=self.gss_codes)
        for polling_station_id, uprns in polling_station_lookup.items():
            uprns_assigned_to_station = uprns_in_council.filter(uprn__in=uprns)

            if self.extra_councils:
                self.set_polling_station_for_extra_councils(
                    polling_station_id, uprns_assigned_to_station
                )

            uprns_assigned_to_station.filter(uprn__in=uprns).update(
                polling_station_id=polling_station_id
            )

    def set_polling_station_for_extra_councils(
        self, polling_station_id, uprns_assigned_to_station
    ):
        # At this stage we want to know if the station has the right council id.
        # There are three cases:
        # 1. All the addresses are in the council named in the import script.
        #    So the station will have the correct council_id and no action is necessary.
        # 2. All the addresses are in a different council.
        #    In this case we need to update the council_id on the polling station in the pollingstations table
        # 3. The addresses assigned to this station are in different council areas.
        #    In this case we need to duplicate the station making sure there are a record for each council_id.
        gss_codes = uprns_assigned_to_station.values_list("lad", flat=True)
        council_ids = CouncilGeography.objects.filter(gss__in=gss_codes).values_list(
            "council_id", flat=True
        )
        if len(council_ids) == 1 and council_ids[0] == self.council_id:
            # Case 1 - no-op
            pass
        if len(council_ids) == 1 and council_ids[0] != self.council_id:
            # Case 2 - change council id on station
            station = PollingStation.objects.get(
                internal_council_id=polling_station_id,
                council_id=self.council_id,
            )
            station.council_id = council_ids[0]
            station.save()
        if len(council_ids) > 1:
            # Case 3 - create a station for each council
            for council_id in council_ids:
                try:
                    PollingStation.objects.get(
                        council_id=council_id,
                        internal_council_id=polling_station_id,
                    )
                except PollingStation.DoesNotExist:
                    existing_station = PollingStation.objects.get(
                        council_id=self.council_id,
                        internal_council_id=polling_station_id,
                    )
                    existing_station.id = None
                    existing_station.council_id = council_id
                    existing_station._state.adding = True
                    existing_station.save()

    def check_records(self):
        split_postcodes = self.get_council_split_postcodes()
        self.remove_records_missing_uprns()
        self.remove_duplicate_uprns()
        addressbase_data = get_uprn_hash_table(self.gss_codes)
        self.remove_records_not_in_addressbase(addressbase_data)
        self.remove_records_that_dont_match_addressbase(addressbase_data)
        self.check_split_postcodes_are_split(split_postcodes)
