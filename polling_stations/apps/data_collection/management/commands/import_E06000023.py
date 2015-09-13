import os
import csv
import json
from zipfile import ZipFile

from fastkml import kml
import shapely


from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point, GEOSGeometry

import geomet

from pollingstations.models import PollingStation, PollingDistrict

class Command(BaseCommand):
    def import_areas(self):
        filename = os.path.abspath(
         'data/bristol_areas.kmz'
        )
        kmz = ZipFile(filename, 'r')
        kml_file = kmz.open('doc.kml', 'r')
        k = kml.KML()
        k.from_string(kml_file.read())
        main = next(k.features())
        districts = next(main.features())

        council_id = "E06000023"
        for district in districts.features():
            polygons = district.geometry.wkt[18:-3].split(')), ((')

            WKT = ""
            for polygon in polygons:
                points = polygon.split(',')
                cleaned_points = ""
                for point in points:
                    split_points = point.strip().split(' ')
                    x = split_points[0]
                    y = split_points[1]
                    cleaned_points += "%s %s, " % (x,y)
                cleaned_points = "((%s))," % cleaned_points[:-2]

                WKT += cleaned_points

            WKT = "MULTIPOLYGON (%s)" % WKT[:-1]
            default_values = {
                'name': district.name,
                'area': WKT,
            }

            PollingDistrict.objects.update_or_create(
                council_id=council_id,
                internal_council_id=district.id,
                defaults=default_values
            )


    def import_stations(self):
        filename = os.path.abspath(
            "data/bristol_polling.json"
        )
        in_file = json.loads(open(filename).read())
        council_id = "E06000023"
        for polling_station in in_file['features']:
            print(polling_station)
            defaults = {
                'location': Point(
                    int(polling_station['geometry']['x']),
                    int(polling_station['geometry']['y']),
                    srid=27700
                ),
                'postcode': polling_station['attributes']['POSTCODE'],
            }

            print([
                polling_station['attributes'].get('LOCATION_NAME', '') or "",
                polling_station['attributes'].get('STREET', '') or "",
                polling_station['attributes'].get('LOCALITY', '') or "",
                polling_station['attributes'].get('TOWN', '') or "",
            ])

            defaults['address'] = "\n".join([
                polling_station['attributes'].get('LOCATION_NAME', '') or "",
                polling_station['attributes'].get('STREET', '') or "",
                polling_station['attributes'].get('LOCALITY', '') or "",
                polling_station['attributes'].get('TOWN', '') or "",
            ])
            print(polling_station['attributes']['UPRN'])
            PollingStation.objects.update_or_create(
                council_id=council_id,
                internal_council_id=polling_station['attributes']['UPRN'] or polling_station['attributes']['LOCATION_NAME'],
                defaults=defaults
            )


    def handle(self, **options):
        self.import_areas()
        self.import_stations()