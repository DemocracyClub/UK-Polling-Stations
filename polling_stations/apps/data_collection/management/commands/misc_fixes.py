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
