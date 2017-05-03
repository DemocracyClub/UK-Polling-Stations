from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from pollingstations.models import PollingStation, PollingDistrict
from councils.models import Council


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        print("updating Torridge phone number...")
        torridge = Council.objects.get(pk='E07000046')
        torridge.phone = "01237 428739"
        torridge.save()
        print("..updated")


        print("updating point for: Manchester Central Library...")
        stations = PollingStation.objects.filter(
            council_id='E08000003',
            internal_council_id='3019'
        )
        if len(stations) == 1:
            station= stations[0]
            station.location = Point(-2.24415, 53.47784, srid=4326)
            station.save()
            print("..updated")
        else:
            print("..NOT updated")


        print("updating point for: CLASSROOM HS210, WALSALL COLLEGE...")
        stations = PollingStation.objects.filter(
            council_id='E08000030',
            internal_council_id='15'
        )
        if len(stations) == 1:
            station= stations[0]
            station.location = Point(-1.984424, 52.590524, srid=4326)
            station.save()
            print("..updated")
        else:
            print("..NOT updated")


        print("..done")
