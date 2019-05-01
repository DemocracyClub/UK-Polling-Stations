from django.core.management.base import BaseCommand

from django.contrib.gis.geos import Point
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress
from councils.models import Council
from addressbase.models import Address, Blacklist


def update_station_point(council_id, station_id, point):
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


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        print("updating Watford address...")
        watford = Council.objects.get(pk="E07000103")
        watford.address = "Electoral Services Office\nRoom 22\nTown Hall\nWatford"
        watford.postcode = "WD17 3EX"
        watford.save()
        print("..updated")

        print("updating Harrogate address...")
        harrogate = Council.objects.get(pk="E07000165")
        harrogate.address = "Civic Centre\nSt Lukes Avenue\nHarrogate"
        harrogate.postcode = "HG1 2AE"
        harrogate.save()
        print("..updated")

        print("updating Oadby & Wigston name...")
        oadby = Council.objects.get(pk="E07000135")
        oadby.name = "Oadby & Wigston Borough Council"
        oadby.save()
        print("..updated")

        print("updating Swansea name...")
        swansea = Council.objects.get(pk="W06000011")
        swansea.name = "City & County of Swansea"
        swansea.save()
        print("..updated")

        print("removing bad points from AddressBase")
        bad_uprns = [
            "10023906550",
            "2630153843",
            "14059977",
            "10007921239",
            "10007920387",
            "10007920390",
            "10024288188",
            "10024288190",
            "10024288189",
            "10023117526",
            "10009922833",
        ]
        addresses = Address.objects.filter(pk__in=bad_uprns)
        for address in addresses:
            print(address.uprn)
            address.delete()
        print("..deleted")

        print("removing dodgy blacklist entries (result of bad point in AddressBase)..")
        blacklist = Blacklist.objects.filter(postcode="RH122LP")
        if len(blacklist) == 2:
            for b in blacklist:
                b.delete()
                print("..deleted")
        else:
            print("..NOT deleted")

        print(
            "removing dodgy blacklist entries (result of bad points in AddressBase).."
        )
        blacklist = Blacklist.objects.filter(postcode="S24AX")
        if len(blacklist) == 2:
            for b in blacklist:
                b.delete()
                print("..deleted")
        else:
            print("..NOT deleted")

        print("updating: Meppershall Village Hall...")
        stations = PollingStation.objects.filter(
            council_id="E06000056", internal_council_id="10361"
        )
        if len(stations) == 1:
            station = stations[0]
            station.location = Point(-0.340481, 52.018151, srid=4326)
            station.address = (
                "Meppershall Village Hall\nWalnut Tree Way\nMeppershall\nSG17 5AB"
            )
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # user issue report #49
        print("updating: WI Hall, Faversham Road...")
        update_station_point("E07000105", "5707", Point(0.885308, 51.169796, srid=4326))

        # user issue report #50
        print("updating: Sandhurst School Sports Hall...")
        update_station_point(
            "E06000036", "4019", Point(-0.782442, 51.350179, srid=4326)
        )

        # user issue report #51
        print("updating: Weobley Village Hall...")
        update_station_point(
            "E06000019",
            "99-weobley-village-hall",
            Point(-2.869103, 52.159915, srid=4326),
        )

        # user issue report #47 (again)
        print("updating: Southill Community Centre...")
        stations = PollingStation.objects.filter(
            council_id="E06000059", internal_council_id="30560"
        )
        if len(stations) == 1:
            station = stations[0]
            station.postcode = "DT4 9SS"
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # user issue report #52
        print("updating: Rhodes Arts Complex...")
        update_station_point("E07000242", "1919", Point(0.163535, 51.863442, srid=4326))

        # user issue report #53
        print("updating: Moose Lodge...")
        update_station_point(
            "E06000059", "30570", Point(-2.466883, 50.606307, srid=4326)
        )

        print("updating: SW&T station 6753...")
        # All those electors who were going to Staplegrove Church School
        # are actually going to
        # Staplegrove Village Hall, 214 Staplegrove Road, Taunton TA2 6AL
        stations = PollingStation.objects.filter(
            council_id="E07000246", internal_council_id="6753"
        )
        if len(stations) == 1:
            station = stations[0]
            station.location = Point(-3.122027, 51.028508, srid=4326)
            station.address = "Staplegrove Village Hall\n214 Staplegrove Road\nTaunton"
            station.postcode = "TA2 6AL"
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        deleteme = [
            # nothing yet
        ]
        for council_id in deleteme:
            print("Deleting data for council %s..." % (council_id))
            # check this council exists
            c = Council.objects.get(pk=council_id)
            print(c.name)

            PollingStation.objects.filter(council=council_id).delete()
            PollingDistrict.objects.filter(council=council_id).delete()
            ResidentialAddress.objects.filter(council=council_id).delete()
            print("..deleted")

        print("..done")
