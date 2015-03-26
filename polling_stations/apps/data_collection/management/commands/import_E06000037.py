import os
import csv

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from pollingstations.models import PollingStation, PollingDistrict

class Command(BaseCommand):
    def handle(self, **options):
        filename = "/Users/symroe/Downloads/polling_stations.xlsx - rubExport_Output_9.csv"
        in_file = csv.DictReader(open(filename))
        council_id = "E06000037"
        for polling_station in in_file:

            defaults = {
                'location': Point(
                    int(polling_station['PSX']),
                    int(polling_station['PSY']),
                    srid=27700
                ),
                'address': polling_station['PSTATION'],
                'postcode': " ".join(polling_station['PSTATION'].split(' ')[-2:])
            }

            PollingStation.objects.update_or_create(
                council_id=council_id,
                internal_council_id=polling_station['PSUPRN'],
                defaults=defaults
            )
