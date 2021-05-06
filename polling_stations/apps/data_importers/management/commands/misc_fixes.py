from django.core.management.base import BaseCommand

# from django.contrib.gis.geos import Point
from pollingstations.models import PollingStation, PollingDistrict
from councils.models import Council
from addressbase.models import Address, UprnToCouncil


def update_station_point(council_id, station_id, point):
    """
    Assigns a new location to station
    'point' should be instance of geos Point
        - Point(x-coord, y-coord, srid=epsg-code)

    If you take the coords from googlemaps then the srid will be 4326
    If you take the coords from BNG then the srid will be 27700

    Points are stored in the database in EPSG: 4326, so use this, or call transform.
    eg Point(-4.4330, 55.9124, srid=4326)
    or Point(248023, 671487, srid=27700).transform(4326)
    """
    stations = PollingStation.objects.filter(
        council_id=council_id, internal_council_id=station_id
    )
    if len(stations) == 1:
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

        # User issue 466
        print(
            "removing location for station: St Philip`s Church (Kensington and Chelsea)..."
        )
        update_station_point("KEC", "939", None)

        # User issue 467
        print(
            "removing location for station: BARNSLEY MBC SPRINGVALE DEPOT (Barnsley)..."
        )
        update_station_point("BNS", "109A", None)

        # User issue 469
        print(
            "removing location for station Barton Road Community Centre (Lancaster)..."
        )
        update_station_point("LAC", "SCEA", None)

        # Council bug report
        # Addresses in Bargate - AA are no longer going to Sembal House, Handel Terrace and
        # are now going to Central Baptist Church Hall, Devonshire Road
        print(
            "Assinging addresses in Bargate - AA (Southampton) to Central Baptist Church Hall"
        )
        assign_addresses_by_district("STH", "AA", "AB")

        # Council issue https://trello.com/c/RZ5jKncZ/513-rutland
        print(
            "change of station from SOUTH LUFFENHAM VILLAGE HALL to THE BOOT INN (Rutland)..."
        )
        update_station_address(
            "RUT",
            "28-south-luffenham-village-hall",
            "The Boot Inn 10, The Street South Luffenham Rutland",
            "LE15 8NX",
        )

        # Council issue
        # changing St Gregory's Social Centre, (behind Church), 63 Broad Street, Sileby, LE7 1GH
        # correct polling place name but incorrect address and postcode
        print("changing address of St Gregory's Social Centre (Charnwood)...")
        update_station_address(
            "CHA",
            "8532",
            "St Gregory's Social Centre, (behind Church), 24 The Banks, Sileby",
            "LE12 7RE",
        )

        # User issue 473
        print("Removing point for Quenington Village Hall (Cotswold)...")
        update_station_point("COT", "17302", None)

        # User issue 476
        print("Removing point for Pudsey Grangefield School (Leeds)...")
        update_station_point("LDS", "10510", None)

        # User issue 114643 (feedback)
        for station_id in ["92", "93", "95"]:
            print(
                f"Removing point for LONG STRATTON TOWN COUNCIL PAVILLION {station_id} (South Norfolk)..."
            )
            update_station_point("SNO", station_id, None)

        # User issue 482
        print("Removing point for Haigh Road Community Centre (Leeds)")
        update_station_point("LDS", "10527", None)

        # Council issue https://twitter.com/NewportCouncil/status/1390223449566625792
        print("Changing location for Portable Unit Layby in front of Shop (Newport)...")
        update_station_address(
            "NWP",
            "11868",
            "Please note the polling station on Heather Road (usually in the portable building by the shops) has been moved to:, The corner of Goya Close and Brangwyn Crescent, Beechwood, Newport",
            "",
        )

        # User issue 486
        print("Removing point for YMCA - Lawnswood Branch (Leeds)...")
        update_station_point("LDS", "10611", None)

        # User issue 487
        print("Removing point for Attleborough Baptist Church (Breckland)...")
        update_station_point("BRE", "9897", None)

        print("*** ...finished applying misc fixes. ***")
