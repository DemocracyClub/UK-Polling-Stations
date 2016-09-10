import logging
from data_collection.slugger import Slugger
from pollingstations.models import (
    PollingStation,
    PollingDistrict,
    ResidentialAddress
)


class CustomList:
    def __init__(self):
        self.elements = []

    def append(self, element):
        self.elements.append(element)


class StationList(CustomList):

    def save(self):
        stations_db = []
        for station in self.elements:
            record = PollingStation(**station)
            stations_db.append(record)
        PollingStation.objects.bulk_create(stations_db)


class DistrictList(CustomList):

    def save(self):
        districts_db = []
        for district in self.elements:
            record = PollingDistrict(**district)
            districts_db.append(record)
        PollingDistrict.objects.bulk_create(districts_db)


class AddressList(CustomList):

    def __init__(self, logger):
        super().__init__()
        self.seen = set()
        self.logger = logger

    def append(self, address):
        if address['slug'] not in self.seen:
            self.elements.append(address)
            self.seen.add(address['slug'])
        else:
            self.logger.log_message(
                logging.DEBUG, "Duplicate address found:\n%s",
                variable=address, pretty=True)

    def remove_ambiguous_addresses(self, in_addresses):
        tmp_addresses = in_addresses  # lists are passed by reference in python
        address_lookup = {}
        out_addresses = []

        # for each address, build a lookup of address -> list of station ids
        for i in range(0, len(tmp_addresses)):
            record = tmp_addresses[i]
            address_slug = Slugger.slugify(
                "-".join([record['address'], record['postcode']]))
            tmp_addresses[i]['address_slug'] = address_slug
            if address_slug in address_lookup:
                address_lookup[address_slug].append(
                    record['polling_station_id'])
            else:
                address_lookup[address_slug] = [record['polling_station_id']]

        # discard any addresses which map to >1 polling station
        for record in tmp_addresses:
            address_slug = record['address_slug']
            if len(address_lookup[address_slug]) == 1:
                out_addresses.append(record)
            else:
                self.logger.log_message(
                    logging.INFO, "Ambiguous addresses discarded: %s: %s",
                    variable=(address_slug, address_lookup[address_slug]))

        return out_addresses

    def save(self, batch_size):

        self.elements = self.remove_ambiguous_addresses(self.elements)
        addresses_db = []

        for address in self.elements:
            record = ResidentialAddress(
                address=address['address'],
                postcode=address['postcode'],
                polling_station_id=address['polling_station_id'],
                council=address['council'],
                slug=address['slug']
            )
            addresses_db.append(record)

        ResidentialAddress.objects.bulk_create(
            addresses_db, batch_size=batch_size)
