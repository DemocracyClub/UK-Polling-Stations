from pollingstations.models import PollingDistrict, ResidentialAddress
from addressbase.models import Address

def district_contains_all_points(district, points):
    return all([district.area.contains(p) for p in points])

def postcodes_not_contained_by_district(district):
    not_contained = []
    for postcode in Address.objects.postcodes_for_district(district):
        points = Address.objects.points_for_postcode(postcode)
        if not district_contains_all_points(district, points):
            not_contained.append(postcode)
    return not_contained

def districts_requiring_address_lookup(council):
    postcode_report = {
        'no_attention_needed': 0,
        'address_lookup_needed': {},
    }

    for district in PollingDistrict.objects.filter(council=council):
        not_contained = postcodes_not_contained_by_district(district)
        if not_contained:
            postcode_report['address_lookup_needed'][district.name] \
                = not_contained
        else:
            postcode_report['no_attention_needed'] += 1
    return postcode_report

def make_addresses_for_postcode(postcode):
    addresses = Address.objects.filter(postcode=postcode)
    for address in addresses:
        district = PollingDistrict.objects.get(area__covers=address.location)
        polling_station_id = district.polling_station_id
        residential_address, _ = ResidentialAddress.objects.get_or_create(
            slug=address.uprn,
            defaults={
                'address': address.address,
                'postcode': postcode,
                'council': district.council,
                'polling_station_id': polling_station_id,
            }
        )
