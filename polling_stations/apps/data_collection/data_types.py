"""
Data type classes used by base importers
"""

import abc
import logging
from collections import namedtuple
from data_collection.slugger import Slugger
from pollingstations.models import (
    PollingStation,
    PollingDistrict,
    ResidentialAddress
)


Station = namedtuple('Station', [
    'council',
    'internal_council_id',
    'postcode',
    'address',
    'location',
    'polling_district_id'])


District = namedtuple('District', [
    'name',
    'council',
    'internal_council_id',
    'extra_id',
    'area',
    'polling_station_id'])


Address = namedtuple('Address', [
    'address',
    'postcode',
    'council',
    'polling_station_id',
    'slug'])


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
        if 'location' in element and element['location']:
            location = element['location'].ewkb  # use ewkb so it encodes srid
        else:
            location = None

        return Station(
            element['council'],
            element['internal_council_id'],
            element.get('postcode', ''),
            element.get('address', ''),
            location,
            element.get('polling_district_id', ''),
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
        area = element['area'].ewkb  # use ewkb so it encodes srid

        return District(
            element.get('name', ''),
            element['council'],
            element['internal_council_id'],
            element.get('extra_id', ''),
            area,
            element.get('polling_station_id', ''),
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


class AddressSet(CustomSet):

    def __init__(self, logger):
        super().__init__()
        self.seen = set()
        self.logger = logger

    def build_namedtuple(self, element):
        return Address(
            element['address'],
            element['postcode'],
            element['council'],
            element['polling_station_id'],
            element['slug'],
        )

    def add(self, address):
        if address['slug'] not in self.seen:
            self.elements.add(self.build_namedtuple(address))
            self.seen.add(address['slug'])
        else:
            self.logger.log_message(
                logging.DEBUG, "Duplicate address found:\n%s",
                variable=address, pretty=True)

    def get_address_lookup(self, addresses):
        # for each address, build a lookup of address -> list of station ids
        address_lookup = {}
        for i, record in enumerate(addresses):
            address_slug = Slugger.slugify(
                "-".join([record['address'], record['postcode']]))
            addresses[i]['address_slug'] = address_slug
            if address_slug in address_lookup:
                address_lookup[address_slug].append(
                    record['polling_station_id'])
            else:
                address_lookup[address_slug] = [record['polling_station_id']]

        return address_lookup

    def get_ambiguous_postcodes(self, address_list, address_lookup):
        # build a set of postcodes containing
        # an address that maps to >1 polling stations
        ambiguous_postcodes = set()
        for record in address_list:
            if len(address_lookup[record['address_slug']]) != 1:
                ambiguous_postcodes.add(record['postcode'])

        return ambiguous_postcodes

    def remove_ambiguous_addresses(self):

        # convert our set of tuples into a list of dicts
        tmp_addresses = list(self.elements)
        tmp_addresses = [x._asdict() for x in tmp_addresses]

        address_lookup = self.get_address_lookup(tmp_addresses)
        ambiguous_postcodes = self.get_ambiguous_postcodes(tmp_addresses, address_lookup)
        out_addresses = set()

        # discard all addresses with an ambiguous postcode
        for i, record in enumerate(tmp_addresses):
            if record['postcode'] in ambiguous_postcodes:
                tmp_addresses[i] = None
                if len(address_lookup[record['address_slug']]) != 1:
                    # we discard it because the address itself is ambiguous
                    reason = address_lookup[record['address_slug']]
                else:
                    # we've discarded it because it has the same postcode
                    # as some other addresses we have discarded
                    reason = record['postcode']

                self.logger.log_message(
                    logging.INFO, "Ambiguous addresses discarded: %s: %s",
                    variable=(record['address_slug'], reason))

        for record in tmp_addresses:
            if record:
                out_addresses.add(self.build_namedtuple(record))

        return out_addresses

    def save(self, batch_size):

        self.elements = self.remove_ambiguous_addresses()
        addresses_db = []

        for address in self.elements:
            record = ResidentialAddress(
                address=address.address,
                postcode=address.postcode,
                polling_station_id=address.polling_station_id,
                council=address.council,
                slug=address.slug,
            )
            addresses_db.append(record)

        ResidentialAddress.objects.bulk_create(
            addresses_db, batch_size=batch_size)
