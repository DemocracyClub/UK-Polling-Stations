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

        print("..done")
