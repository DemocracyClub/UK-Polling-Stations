import logging
from collections import namedtuple
from django.db import connection
from councils.models import Council
from pollingstations.models import (PollingDistrict, ResidentialAddress,
                                    PollingStation)
from pollingstations.helpers import format_postcode_no_space
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


class AddressSet(set):

    def save(self, batch_size):

        addresses_db = []
        for address in self:
            record = ResidentialAddress(
                address=address.address,
                postcode=format_postcode_no_space(address.postcode),
                polling_station_id=address.polling_station_id,
                council_id=address.council_id,
                slug=address.slug,
            )
            addresses_db.append(record)

        ResidentialAddress.objects.bulk_create(
            addresses_db, batch_size=batch_size)


class EdgeCaseFixer:

    def __init__(self, target_council_id, logger):
        self.address_set = AddressSet()
        self.target_council_id = target_council_id
        self.logger = logger
        self.AddressRecord = namedtuple('AddressRecord', [
            'uprn',
            'address',
            'postcode',
            'district_id',
            'station_id',
            'council_id',
            'count',
            'location',
        ])

    def unpack_address(self, record):
        return self.AddressRecord(*record)

    def get_station_id(self, address):
        if not address.council_id:
            c = Council.objects\
                .defer("area", "location")\
                .get(area__covers=address.location)
            council_id = c.council_id
        else:
            council_id = address.council_id

        if council_id != self.target_council_id:
            # treat addresses in other council areas as district not found
            raise PollingDistrict.DoesNotExist

        if address.count > 1:
            raise PollingDistrict.MultipleObjectsReturned

        if not address.district_id:
            raise PollingDistrict.DoesNotExist

        if address.station_id:
            polling_station = address.station_id
        else:
            """
            We do not know which station this district is served by (orphan district)

            Because we have no way of knowing what the correct station is, intentionally insert a record with an empty station id
            This allows us to *list* the address, but if the user *chooses* it, we will show "we don't know: call your council"
            """
            polling_station = ''

        return polling_station

    def make_addresses_for_postcode(self, postcode):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                ab.uprn,
                ab.address,
                ab.postcode,
                pd.internal_council_id,
                ps.internal_council_id,
                os.lad,
                ct.count,
                ab.location
            FROM addressbase_address ab

            LEFT JOIN pollingstations_pollingdistrict pd
            ON ST_CONTAINS(pd.area, ab.location)

            LEFT JOIN uk_geo_utils_onsud os
            ON os.uprn=ab.uprn

            LEFT JOIN pollingstations_pollingstation ps
            ON (
                (pd.polling_station_id=ps.internal_council_id
                    AND pd.council_id=ps.council_id)
                OR
                (pd.internal_council_id=ps.polling_district_id
                    AND pd.council_id=ps.council_id)
            )

            JOIN (
                SELECT
                    ab.uprn,
                    COUNT(*) AS count
                FROM addressbase_address ab
                LEFT JOIN pollingstations_pollingdistrict pd
                ON ST_CONTAINS(pd.area, ab.location)
                WHERE ab.postcode=%s
                GROUP BY ab.uprn
            ) ct
            ON ab.uprn=ct.uprn

            WHERE ab.postcode=%s
            """, [postcode, postcode]
        )
        addresses = cursor.fetchall()

        for record in addresses:
            address = self.unpack_address(record)
            try:
                station_id = self.get_station_id(address)
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

                self.logger.log_message(
                    logging.WARNING,
                    "Found address contained by >1 polling districts - data may contain overlapping polygons:\n%s\n%s\n",
                    variable=(address.address, address.postcode))

                station_id = ''
            except Council.DoesNotExist:
                self.logger.log_message(
                    logging.WARNING,
                    "Skipping address which could not be assigned to a local authority:\n%s\n%s\n",
                    variable=(address.address, address.postcode))
                continue

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


def create_address_records_for_council(council, batch_size, logger):
    postcode_report = {
        'no_attention_needed': 0,
        'addresses_created': 0,
        'postcodes_needing_address_lookup': set(),
    }

    fixer = EdgeCaseFixer(council.pk, logger)
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


class AddressFormatter:

    def __init__(
            self,
            organisation_name,
            department_name,
            po_box_number,
            sub_building_name,
            building_name,
            building_number,
            dependent_thoroughfare,
            thoroughfare,
            post_town,
            double_dependent_locality,
            dependent_locality,
            ):
        """one to one mapping."""
        self.organisation_name = organisation_name
        self.department_name = department_name
        self.po_box_number = po_box_number
        self.sub_building_name = sub_building_name
        self.building_name = building_name
        self.building_number = building_number
        self.dependent_thoroughfare = dependent_thoroughfare
        self.thoroughfare = thoroughfare
        self.post_town = post_town
        self.double_dependent_locality = double_dependent_locality
        self.dependent_locality = dependent_locality
        self.address_label = []

    def generate_address_label(self):
        """Construct a list for address label.

        Non-empty premises elements are appended to the address label in the
        order of organisation_name, department_name, po_box_number (which
        must be prepended with 'PO Box', sub_building_name, building_name,
        building_number, then the rest of the elements except for Town and
        Postcode because we want them in their own fields. This isn't strict
        address label but we're probably loading them into a database.
        """
        if self.organisation_name:
            self.address_label.append(self.organisation_name)
        if self.department_name:
            self.address_label.append(self.department_name)
        if self.po_box_number:
            self.address_label.append('PO Box ' + self.po_box_number)

        elements = [
                self.sub_building_name,
                self.building_name,
                self.building_number,
                self.dependent_thoroughfare,
                self.thoroughfare,
                self.double_dependent_locality,
                self.dependent_locality,
        ]

        for element in elements:
            if element:
                self._append_to_label(element)

        # pad label to length of 7 if not already
        if len(self.address_label) < 7:
            for i in range(7 - len(self.address_label)):
                self.address_label.append('')

        # finally, add post town
        self.address_label[5] = self.post_town

        return ", ".join([f for f in self.address_label if f])

    def _is_exception_rule(self, element):
        """ Check for "exception rule".

        Address elements will be appended onto a new line on the lable except
        for when the penultimate lable line fulfils certain criteria, in which
        case the element will be concatenated onto the penultimate line. This
        method checks for those criteria.

        i) First and last characters of the Building Name are numeric
          (eg '1to1' or '100:1')
        ii) First and penultimate characters are numeric, last character is
          alphabetic (eg '12A')
        iii) Building Name has only one character (eg 'A')
        """
        if element[0].isdigit() and element[-1].isdigit():
            return True
        if element[0].isdigit() and element[-2].isdigit() and element[-1].isalpha():
            return True
        if len(element) == 1 and element.isalpha():
            return True
        return False

    def _append_to_label(self, element):
        """Append address element to the label.

        Normally an element will be appended onto the list, except where the
        existing last element fulfils the exception rule, in which case the
        element will be concatenated onto the final list member.
        """
        if len(self.address_label) > 0\
                and self._is_exception_rule(self.address_label[-1]):
            self.address_label[-1] += (' ' + element)
        else:
            self.address_label.append(element)

    def __str__(self):
        """Return the label form of the address."""
        return ','.join(self.generate_address_label())
