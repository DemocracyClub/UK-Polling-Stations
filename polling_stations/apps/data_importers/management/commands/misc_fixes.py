from addressbase.models import Address, UprnToCouncil
from councils.models import Council
from django.core.management.base import BaseCommand
from pollingstations.models import PollingDistrict, PollingStation


def update_station_point(council_id, station_id, point):
    """
    Assigns a new location to station
    'point' should be an instance of geos Point
        - Point(x-coord, y-coord, srid=epsg-code)

    If you take the coords from googlemaps then the srid will be 4326
    If you take the coords from BNG then the srid will be 27700

    Points are stored in the database in EPSG: 4326, so use this, or call transform.
    eg point=Point(-4.4330, 55.9124, srid=4326)
    or point=Point(248023, 671487, srid=27700).transform(4326, clone=True)

    If you don't include 'clone=True', the transform method returns None.
    """
    stations = PollingStation.objects.filter(
        council_id=council_id, internal_council_id=station_id
    )
    if len(stations) == 1:
        if not point:
            print("Setting station location to None")
        station = stations[0]
        station.location = point
        station.save()
        print("..updated")
    else:
        print("..NOT updated")


def update_station_address(
    council_id,
    station_id,
    address="",
    postcode="",
):
    """
    Updates address and postcode.
    Can be used to just update postcode if no address is provided
    """
    stations = PollingStation.objects.filter(
        council_id=council_id, internal_council_id=station_id
    )
    if len(stations) == 1:
        station = stations[0]
        station.address = address if address else station.address
        station.postcode = postcode
        station.save()
        print("..updated")
    else:
        print("..NOT updated")


def assign_addresses_by_district(council_id, district_id, station_id):
    """
    Sets uprntocouncil.polling_station_id to station_id for all uprns in district
    NB PollingStation(council_id, station_id) must exist
    """
    districts = PollingDistrict.objects.filter(
        council_id=council_id, internal_council_id=district_id
    )
    stations = PollingStation.objects.filter(
        council_id=council_id, internal_council_id=station_id
    )
    if len(districts) and len(stations) == 1:
        district = districts[0]
        uprns = UprnToCouncil.objects.filter(uprn__location__within=district.area)
        uprns.update(polling_station_id=station_id)
        print("...updated")
    else:
        print("..NOT updated")


def unassign_addresses_by_district(council_id, district_id):
    """
    Sets uprntocouncil.polling_station_id to "" for all uprns in district
    """
    districts = PollingDistrict.objects.filter(
        council_id=council_id, internal_council_id=district_id
    )
    if len(districts) == 1:
        district = districts[0]
        uprns = UprnToCouncil.objects.filter(uprn__location__within=district.area)
        uprns.update(polling_station_id="")
        print("...updated")
    else:
        print("..NOT updated")


def unassign_uprns(uprns_to_unassign):
    uprns = UprnToCouncil.objects.filter(pk__in=uprns_to_unassign)
    for uprn in uprns:
        print(uprn.pk)
    uprns.update(polling_station_id="")
    print("...updated")


def unassign_uprns_for_single_station(council_id, station_id):
    uprns = UprnToCouncil.objects.filter(
        lad=Council.objects.get(council_id=council_id).geography.gss,
        polling_station_id=station_id,
    )
    uprns.update(polling_station_id="")
    print("...updated")


def remove_points_from_addressbase(bad_uprns):
    addresses = Address.objects.filter(pk__in=bad_uprns)
    for address in addresses:
        print(address.uprn)
        address.delete()
    print("..deleted")
    print("removing bad uprns from uprn lookup")
    uprns = UprnToCouncil.objects.filter(pk__in=bad_uprns)
    for uprn in uprns:
        print(uprn.pk)
        uprn.delete()
    print(".. deleted")


def delete_council_data(council_id):
    # check this council exists
    c = Council.objects.get(pk=council_id)
    print(c.name)

    PollingStation.objects.filter(council=council_id).delete()
    PollingDistrict.objects.filter(council=council_id).delete()
    UprnToCouncil.objects.filter(lad=c.geography.gss).update(polling_station_id="")
    print("..deleted")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("*** Applying misc fixes... ***")
        print("removing bad points from AddressBase")
        bad_uprns = [
            "10033560031",  # Addressbase contains individual's name
        ]
        remove_points_from_addressbase(bad_uprns)

        deleteme = [
            # nothing yet
        ]
        for council_id in deleteme:
            print("Deleting data for council %s..." % (council_id))

        print("..done")

        # http://wheredoivote.co.uk/admin/feedback/feedback/83100/change/
        print("Removing point for Otley Social Club")
        update_station_point("LDS", "18998", None)

        print("*** ...finished applying misc fixes. ***")
