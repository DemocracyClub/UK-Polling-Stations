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


def make_addresses_for_postcode(postcode, council_id):
    addresses = Address.objects.filter(postcode=postcode)
    created = 0
    for address in addresses:
        try:
            district = PollingDistrict.objects.get(
                area__covers=address.location, council_id=council_id)
        except PollingDistrict.DoesNotExist:
            # Chances are this is on the edge of the council area, and
            # we don't have data for the are the property is in
            continue
        except PollingDistrict.MultipleObjectsReturned:
            # This is normally causes by districts the overlap
            # Because we have no way of knowing what the correct district is,
            # we need to ignore this address
            continue

        polling_station = PollingStation.objects.get_polling_station(
            district.council.pk,
            polling_district=district)

        if not polling_station:
            # This station doesn't fall inside a district, ignore it
            continue

        residential_address, _ = ResidentialAddress.objects.get_or_create(
            slug=address.uprn,
            defaults={
                'address': address.address,
                'postcode': postcode,
                'council': district.council,
                'polling_station_id': polling_station.internal_council_id,
            }
        )
        created += 1
    return created

def create_address_records_for_council(council):
    postcode_report = {
        'no_attention_needed': 0,
        'addresses_created': 0,
        'postcodes_needing_address_lookup': set(),
    }

    for district in PollingDistrict.objects.filter(council=council):
        data = postcodes_not_contained_by_district(district)

        postcode_report['no_attention_needed'] += \
            data['total'] - len(data['not_contained'])

        for postcode in data['not_contained']:
            postcode_report['postcodes_needing_address_lookup'].add(postcode)
            created = make_addresses_for_postcode(postcode, council.pk)
            postcode_report['addresses_created'] = created

    return postcode_report
