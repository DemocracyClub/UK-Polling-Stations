from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from pollingstations.models import PollingStation, PollingDistrict
from councils.models import Council


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        pass
