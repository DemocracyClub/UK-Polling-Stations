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

        print("updating Torridge phone number...")
        torridge = Council.objects.get(pk='E07000046')
        torridge.phone = "01237 428739"
        torridge.save()
        print("..updated")


        print("updating Torfaen phone number...")
        torfaen = Council.objects.get(pk='W06000020')
        torfaen.phone = "01495 762200"
        torfaen.save()
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


        print("updating: Corfe Mullen Village Hall...")
        stations = PollingStation.objects.filter(
            council_id='E07000049',
            internal_council_id__in= ['5329', '5333']
        )
        if len(stations) == 2:
            for station in stations:
                station.location = Point(-2.017191, 50.7748038, srid=4326)
                station.address = 'Corfe Mullen Village Hall\nTowers Way\nCorfe Mullen\nWimborne'
                station.postcode = 'BH21 3UA'
                station.save()
                print("..updated")
        else:
            print("..NOT updated")


        print("updating point for: Carlton Road United Reformed Church...")
        update_station_point('E06000015', '6305',
            Point(-1.4980912, 52.9057198, srid=4326))


        print("updating: Tilehurst Village Hall...")
        stations = PollingStation.objects.filter(
            council_id='E06000038',
            internal_council_id='2494'
        )
        if len(stations) == 1:
            station = stations[0]
            station.location = Point(-1.040355, 51.460535, srid=4326)
            station.address = 'Tilehurst Village Hall\n17 Victoria Road\nTilehurst\nReading\nRG31 5AB'
            station.save()
            print("..updated")
        else:
            print("..NOT updated")


        print("removing point for: Muslim Khatri Association Community Centre...")
        update_station_point('E06000016', '5379', None)


        print("removing point for: Kingston College, Richmond Road Centre...")
        update_station_point('E09000021', '3426', None)


        print("updating point for: Warwickshire Shopping Park...")
        update_station_point('E08000026', '8115',
            Point(-1.433619, 52.398430, srid=4326))


        print("updating point for: St. Thomas' Church Hall, Islington...")
        update_station_point('E09000019', '1213',
            Point(-0.104049, 51.560139, srid=4326))


        print("updating point for: Hove Town Hall...")
        update_station_point('E06000043', '4515',
            Point(-0.1712095, 50.8287022, srid=4326))


        print("updating point for: Sir Francis Drake Primary School...")
        update_station_point('E09000023', '13422',
            Point(-0.041439, 51.485670, srid=4326))


        print("updating point for: University of Warwick - Oculus Building...")
        update_station_point('E08000026', '8423',
            Point(-1.5598858, 52.3799439, srid=4326))


        print("removing point for: Sleaford Leisure Centre...")
        update_station_point('E07000139', '4421', None)


        print("updating point for: St. Joseph's R.C Church Hall...")
        update_station_point('W06000012', '90-st-josephs-rc-church-hall',
            Point(-3.800506, 51.6536899, srid=4326))


        print("updating point for: Watton Sports Association...")
        update_station_point('E07000143', '5854',
            Point(0.827944, 52.574566, srid=4326))


        print("updating point for: St John The Baptist Church Hall...")
        update_station_point('E07000091', '6913',
            Point(-1.767228, 50.8546796, srid=4326))


        print("updating point for: Eastney Methodist Church...")
        update_station_point('E06000044', '3021',
            Point(-1.059545, 50.7866578, srid=4326))


        print("updating point for: Kingston College...")
        update_station_point('E09000021', '3426',
            Point(-0.3009045, 51.4146479, srid=4326))


        print("updating point for: Church of the Good Shepard (1)...")
        update_station_point('E09000029', '74-the-church-of-the-good-shepherd',
            Point(-0.1691277, 51.35325, srid=4326))
        print("updating point for: Church of the Good Shepard (2)...")
        update_station_point('E09000029', '75-the-church-of-the-good-shepherd',
            Point(-0.1691277, 51.35325, srid=4326))


        print("updating point for: Chepstow Community Centre, Milton Keynes...")
        update_station_point('E06000042', '4861',
            Point(-0.7692866, 51.9892058, srid=4326))


        print("updating: St Andrew's Church, Calderdale...")
        stations = PollingStation.objects.filter(
            council_id='E08000033',
            internal_council_id='FF'
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "St. Andrew's Church, Beechwood Road, Holmfield, Halifax. HX2 9AR"
            station.save()
            print("..updated")
        else:
            print("..NOT updated")


        print("updating: RA, Camden...")
        stations = PollingStation.objects.filter(
            council_id='E09000007',
            internal_council_id='RA'
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Dragon Hall\nStukeley Street"
            station.postcode = "WC2B 5LL"
            station.location = GEOSGeometry('0101000020E610000093C9A99D616ABFBFD7F7E12021C24940')
            station.save()
            print("..updated")
        else:
            print("..NOT updated")


        print("updating: Bennett Court Tenants Hall...")
        stations = PollingStation.objects.filter(
            council_id='E09000019',
            internal_council_id='1186'
        )
        if len(stations) == 1:
            station = stations[0]
            station.postcode = "N7 6BN"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")


        print("updating point for: St John's Hill Residents Centre...")
        update_station_point('E09000032', '5645',
            Point(-0.1699533, 51.4622247, srid=4326))


        print("updating point for: High Hill Estate Community Hall...")
        update_station_point('E09000012', '2297',
            Point(-0.0542398, 51.5677442, srid=4326))


        print("updating point for: Mission Grove South Site...")
        update_station_point('E09000031', '2622',
            Point(-0.025035, 51.581813, srid=4326))


        print("updating point for: The Coach House, Littleborough...")
        update_station_point('E08000005', '1522',
            Point(-2.0961003, 53.6444469, srid=4326))


        print("adding note to: North Finchley Library...")
        stations = PollingStation.objects.filter(
            council_id='E09000003', internal_council_id__in=['B55', 'B54/1'])
        if len(stations) == 2:
            for station in stations:
                station.address = "North Finchley Library (Open despite refurbishment)\nRavensdale Avenue\nNorth Finchley\nLondon"
                station.save()
                print("..updated")
        else:
            print("..NOT updated")


        print("updating Albany Road Primary School --> Mackintosh Community Centre")
        stations = PollingStation.objects.filter(
            council_id='W06000015', internal_council_id__in=['C37-EE', 'C37-EB', 'C37-EG'])
        if len(stations) == 3:
            for station in stations:
                station.address = "Mackintosh Community Centre\nKeppoch Street\nRoath\nCardiff\nCF24 3JW"
                station.location = None
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


        print("adding manual override for AL55FE...")
        addresses = ResidentialAddress.objects.filter(postcode='AL55FE')
        if len(addresses) == 0:
            record = ResidentialAddress(
                address='AL55FE',
                postcode='AL55FE',
                polling_station_id='HBD',
                council_id='E07000240',
                slug='e07000240-hbd-al55fe',
            )
            record.save()
            print('..fixed')
        else:
            print('..NOT fixed')


        print("..done")
