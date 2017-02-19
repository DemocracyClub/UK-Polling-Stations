import re
from collections import namedtuple
from pollingstations.models import (PollingDistrict, ResidentialAddress,
                                    PollingStation)
from addressbase.models import Address


def centre_from_points_qs(qs):
    if not qs:
        return None

    if len(qs) == 1:
        return qs[0].location

    base_point = qs[0].location
    poly = base_point.union(qs[1].location)
    for m in qs:
        poly = poly.union(m.location)

    return poly.centroid


AddressTuple = namedtuple('Address', [
    'address',
    'postcode',
    'council_id',
    'polling_station_id',
    'slug'])


class AddressSet:

    def __len__(self):
        return len(self.elements)

    def __init__(self):
        self.elements = set()

    def add(self, address):
        self.elements.add(address)

    def save(self, batch_size):

        addresses_db = []
        for address in self.elements:
            record = ResidentialAddress(
                address=address.address,
                postcode=re.sub('[^A-Z0-9]', '', address.postcode),
                polling_station_id=address.polling_station_id,
                council_id=address.council_id,
                slug=address.slug,
            )
            addresses_db.append(record)

        ResidentialAddress.objects.bulk_create(
            addresses_db, batch_size=batch_size)


class EdgeCaseFixer:

    def __init__(self, target_council_id):
        self.address_set = AddressSet()
        self.target_council_id = target_council_id

    def get_station_id(self, location):
        district = PollingDistrict.objects.get(
            area__covers=location, council_id=self.target_council_id)

        polling_station = PollingStation.objects.get_polling_station(
            district.council.pk,
            polling_district=district)

        if not polling_station:
            """
            We do not know which station this district is served by (orphan district)

            Because we have no way of knowing what the correct station is, intentionally insert a record with an empty station id
            This allows us to *list* the address, but if the user *chooses* it, we will show "we don't know: call your council"
            """
            return ''

        return polling_station.internal_council_id

    def make_addresses_for_postcode(self, postcode):
        addresses = Address.objects.filter(postcode=postcode)
        for address in addresses:
            try:
                station_id = self.get_station_id(address.location)
            except PollingDistrict.DoesNotExist:
                # Chances are this is on the edge of the council area, and
                # we don't have data for the area the property is in
                # TODO: handle this
                continue
            except PollingDistrict.MultipleObjectsReturned:
                """
                This is normally caused by districts that overlap

                Because we have no way of knowing what the correct station is, intentionally insert a record with an empty station id
                This allows us to *list* the address, but if the user *chooses* it, we will show "we don't know: call your council"
                """
                station_id = ''

            self.address_set.add(AddressTuple(
                address.address,
                postcode,
                self.target_council_id,
                station_id,
                address.uprn,
            ))

    def get_address_set(self):
        return self.address_set


def district_contains_all_points(district, points):
    return all([district.area.contains(p) for p in points])


def postcodes_not_contained_by_district(district):
    data = {
        'not_contained': [],
        'total': 0
    }

    for postcode in Address.objects.postcodes_for_district(district):
        points = Address.objects.points_for_postcode(postcode)
        data['total'] += 1
        if not district_contains_all_points(district, points):
            data['not_contained'].append(postcode)
    return data


def create_address_records_for_council(council, batch_size):
    postcode_report = {
        'no_attention_needed': 0,
        'addresses_created': 0,
        'postcodes_needing_address_lookup': set(),
    }

    fixer = EdgeCaseFixer(council.pk)
    for district in PollingDistrict.objects.filter(council=council):
        data = postcodes_not_contained_by_district(district)

        postcode_report['no_attention_needed'] += \
            data['total'] - len(data['not_contained'])
        postcode_report['postcodes_needing_address_lookup'].update(data['not_contained'])

        for postcode in data['not_contained']:
            fixer.make_addresses_for_postcode(postcode)

    address_set = fixer.get_address_set()
    address_set.save(batch_size)
    postcode_report['addresses_created'] = len(address_set)

    return postcode_report
