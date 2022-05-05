from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

# from django.contrib.gis.geos import Point
from pollingstations.models import PollingStation, PollingDistrict
from councils.models import Council
from addressbase.models import Address, UprnToCouncil


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

        # User issue 530 - https://trello.com/c/tYHaUP2O/596-user-report-530
        print("Changing address and location for Temporary building, Kara st (Salford)")
        update_station_address(
            council_id="SLF",
            station_id="6406",
            address="Temporary Building, Alexander Street, Salford",
            postcode="M6 5PY",
        )

        update_station_point(
            council_id="SLF",
            station_id="6406",
            point=Point(380295, 398754, srid=27700).transform(4326, clone=True),
        )

        # User issue 528 - https://trello.com/c/wXII0Fn2/594-user-report-528
        print("Correcting point for Newton Childrens Centre (St Helens)")
        update_station_point(
            council_id="SHN",
            station_id="4831",
            point=Point(357498, 395524, srid=27700).transform(4326, clone=True),
        )

        # User issue https://trello.com/c/xZSwX0qz/595-user-report-l24-4bh
        print("Removing point for Hale Village Hall (Halton)")
        update_station_point(
            council_id="HAL",
            station_id="2845",
            point=None,
        )

        # User issue https://wheredoivote.co.uk/admin/bug_reports/bugreport/534/change/
        print(
            "Updating point for  Mobile station @ corner of Corncrake/Mallards Way (Cherwell)"
        )
        update_station_point(
            council_id="CHR",
            station_id="24684",
            point=Point(-1.14138768, 51.8951794, srid=4326),
        )

        # User issue https://wheredoivote.co.uk/admin/bug_reports/bugreport/540/change/
        print(
            "Updating point for Trowbridge Senior Citizens Club (a bit more accuracy)"
        )
        update_station_point(
            council_id="HCK",
            station_id="6082",
            point=Point(-0.0292106, 51.5455498, srid=4326),
        )

        # At council request
        print("Better point for Fortismere School")
        update_station_point(
            council_id="HRY",
            station_id="8990",
            point=Point(-0.1498665, 51.5931802, srid=4326),
        )

        # At council request
        print("Removing point for Round Chapel, 1D Glenarm Road, Hackney")
        update_station_point(
            council_id="HCK",
            station_id="6112",
            point=None,
        )

        # User issue https://wheredoivote.co.uk/admin/bug_reports/bugreport/542/change/
        print("Better point for William Bonney Community Centre, Lambeth")
        update_station_point(
            council_id="LBH",
            station_id="6999",
            point=Point(-0.1338591, 51.4611662, srid=4326),
        )

        print("Remove point for St Philip's church (RBKC)")
        update_station_point(
            council_id="KEC",
            station_id="1096",
            point=None,
        )

        # User issue https://wheredoivote.co.uk/admin/bug_reports/bugreport/549/change/
        print("Better point for Dalton Community Centre, Barrow-in-Furness")
        for station_id in ["LA1", "MA1"]:
            update_station_point(
                council_id="BAR",
                station_id=station_id,
                point=Point(-3.1822415, 54.1573844, srid=4326),
            )

        # Poor location for walking directions, reported via Fb
        print("Better point for 4th Worcester Park Scout Hut, LB of Sutton")
        for station_id in ["BA/1", "BA/2"]:
            update_station_point(
                council_id="STN",
                station_id=station_id,
                point=Point(-0.2415592, 51.3748792, srid=4326),
            )

        print("*** ...finished applying misc fixes. ***")
