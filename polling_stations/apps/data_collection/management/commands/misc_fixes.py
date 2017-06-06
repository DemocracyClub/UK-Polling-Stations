from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from addressbase.models import Address, Blacklist
from pollingstations.models import PollingStation, PollingDistrict
from councils.models import Council

def update_station_point(council_id, station_id, point):
    stations = PollingStation.objects.filter(
        council_id=council_id,
        internal_council_id=station_id
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

        print("updating Torridge phone number...")
        torridge = Council.objects.get(pk='E07000046')
        torridge.phone = "01237 428739"
        torridge.save()
        print("..updated")


        print("updating point for: CLASSROOM HS210, WALSALL COLLEGE...")
        update_station_point(
            'E08000030',
            '15-classroom-hs210-the-hub-enter-via-portland-street',
            Point(-1.984424, 52.590524, srid=4326))


        print("updating point for: St Alban's Hall, Oxford...")
        update_station_point('E07000178', '4399',
            Point(-1.232920, 51.740993, srid=4326))


        print("updating point for: C3 Centre, Cambridge...")
        update_station_point('E07000008', '38-c3-centre',
            Point(0.1572, 52.2003, srid=4326))


        print("removing point for: Leckhampstead Village Hall...")
        update_station_point('E06000037', '3109', None)


        print("updating point for: Holybrook Centre...")
        update_station_point('E06000037', '3253',
            Point(-1.0269696, 51.4415176, srid=4326))


        print("updating point for: Cossall Tenants Hall...")
        update_station_point('E09000028', '10223',
            Point(-0.0619122, 51.4715108, srid=4326))


        print("removing point for: Corfe Mullen Village Hall...")
        update_station_point('E07000049', '5329', None)


        print("updating point for: Carlton Road United Reformed Church...")
        update_station_point('E06000015', '6305',
            Point(-1.4980912, 52.9057198, srid=4326))


        print("removing point for: Tilehurst Village Hall...")
        update_station_point('E06000038', '2494', None)


        print("adding note to: North Finchley Library...")
        stations = PollingStation.objects.filter(
            council_id='E09000003', internal_council_id='B55')
        if len(stations) == 1:
            station = stations[0]
            station.address = "North Finchley Library (Open despite refurbishment)\nRavensdale Avenue\nNorth Finchley\nLondon"
            station.save()
            print("..updated")
        else:
            print("..NOT updated")


        print("removing dodgy blacklist entry (result of bad point in AddressBase)..")
        blacklist = Blacklist.objects.filter(postcode='AB115QH')
        if len(blacklist) == 2:
            for b in blacklist:
                b.delete()
                print('..deleted')
        else:
            print('..NOT deleted')


        print("removing bad point from AddressBase (UPRN 10090647993)")
        try:
            address = Address.objects.get(pk='10090647993')
            address.delete()
            print('..deleted')
        except Address.DoesNotExist:
            print('..NOT deleted')


        print("removing bad point from AddressBase (UPRN 10091769090)")
        try:
            address = Address.objects.get(pk='10091769090')
            address.delete()
            print('..deleted')
        except Address.DoesNotExist:
            print('..NOT deleted')


        print("..done")
