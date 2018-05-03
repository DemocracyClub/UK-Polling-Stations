from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry

from addressbase.models import Address, Blacklist
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress
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

        print("updating Westminster Address...")
        westminster = Council.objects.get(pk='E09000033')
        westminster.address = "Electoral Services\nWestminster City Council\n2nd Floor\nCity Hall\n5 Strand\nLondon"
        westminster.postcode = "WC2N 5HR"
        westminster.save()
        print("..updated")

        print("updating Southend email address...")
        southend = Council.objects.get(pk='E06000033')
        southend.email = 'elections@southend.gov.uk'
        southend.save()
        print("..updated")

        print("updating Hull phone number...")
        hull = Council.objects.get(pk='E06000010')
        hull.phone = '01482 300 302'
        hull.save()
        print("..updated")


        print("updating point for: Alf Marshall Community Centre, Hull...")
        update_station_point(
            'E06000010',
            '8515',
            Point(-0.321628, 53.787659, srid=4326))

        print("updating point for: All Saints Church Hall, Hastings...")
        update_station_point(
            'E07000062',
            '23-all-saints-church-hall',
            Point(0.595763, 50.859451, srid=4326))

        print("updating point for: Salvation Army Hall, South Cambs...")
        update_station_point(
            'E07000012',
            '6555',
            Point(0.191974, 52.264660, srid=4326))

        # bug report #5
        print("updating point for: St. Luke's Church Hall, Sefton...")
        update_station_point(
            'E08000014',
            '4529',
            Point(-2.985813, 53.646988, srid=4326))

        # 2x reports from Halton council
        print("updating point for: St Marys Halton Ce Primary School, Halton...")
        update_station_point(
            'E06000006',
            '308',
            Point(-2.690746, 53.331598, srid=4326))

        print("updating: St Edwards Parish Centre, Halton...")
        stations = PollingStation.objects.filter(
            council_id='E06000006',
            internal_council_id='283'
        )
        if len(stations) == 1:
            station = stations[0]
            station.location = Point(-2.728014, 53.335534, srid=4326)
            station.postcode = 'WA7 5PB'
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # bug report #6
        print("updating point for: Holy Trinity Church Centre, Sutton...")
        update_station_point(
            'E09000029',
            'OB_1',
            Point(-0.151435, 51.364474, srid=4326))

        # bug report #7
        print("updating: Berkley Street Methodist Church, Huntingdonshire...")
        stations = PollingStation.objects.filter(
            council_id='E07000011',
            internal_council_id='5860'
        )
        if len(stations) == 1:
            station = stations[0]
            station.location = Point(-0.266772, 52.223385, srid=4326)
            station.postcode = 'PE19 2NB'
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # request from council
        print("updating: St George`s Church, Reading...")
        stations = PollingStation.objects.filter(
            council_id='E06000038',
            internal_council_id='2701'
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "St George`s Church\nSt George`s Road\nTilehurst\nReading\nRG30 2RG"
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # bug report #8
        print("updating point for: Macaulay CE Primary School, Lambeth...")
        update_station_point(
            'E09000022',
            'VHC',
            Point(-0.148103, 51.463782, srid=4326))

        # bug report #9
        print("updating point for: METHODIST CHURCH HALL, Great Yarmouth...")
        update_station_point(
            'E07000145',
            '24-methodist-church-hall',
            Point(1.714309, 52.572677, srid=4326))


        # 2x reports from Islington council
        print("updating point for: St Joan of Arc Community Centre, Islington...")
        update_station_point(
            'E09000019',
            '1401',
            Point(-0.0966823, 51.5559102, srid=4326))

        print("updating: St. Thomas` Church Hall, Islington...")
        stations = PollingStation.objects.filter(
            council_id='E09000019',
            internal_council_id='1404'
        )
        if len(stations) == 1:
            station = stations[0]
            station.postcode = "N4 2QP"
            station.save()
            print("..updated")
        else:
            print("..NOT updated")


        # bug report #12
        print("updating point for: St Mary and Ambrose Church Hall, Birmingham...")
        update_station_point(
            'E08000025',
            '122-st-mary-and-ambrose-church-hall',
            Point(-1.904365, 52.458623, srid=4326))


        print("updating point for: St Cuthbert`s Centre, Kensington & Chelsea...")
        update_station_point(
            'E09000020',
            '672',
            Point(-0.200082, 51.491363, srid=4326))

        # bug report #13
        print("updating point for: Summertown United Reformed Church, Oxford...")
        update_station_point(
            'E07000178',
            '4793',
            Point(-1.265459, 51.778845, srid=4326))



        deleteme = [
            # nothing yet
        ]
        for council_id in deleteme:
            print('Deleting data for council %s...' % (council_id))
            # check this council exists
            c = Council.objects.get(pk=council_id)
            print(c.name)

            PollingStation.objects.filter(council=council_id).delete()
            PollingDistrict.objects.filter(council=council_id).delete()
            ResidentialAddress.objects.filter(council=council_id).delete()
            print('..deleted')


        print("..done")
