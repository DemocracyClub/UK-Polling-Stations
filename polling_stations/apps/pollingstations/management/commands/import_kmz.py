import os
from zipfile import ZipFile

from fastkml import kml
import shapely

from django.core.management.base import BaseCommand

from pollingstations.models import PollingStation, PollingDistrict

class Command(BaseCommand):

    def handle(self, **options):
        filename = "/Users/symroe/Downloads/Polling_Boundaries (1).kmz"
        kmz = ZipFile(filename, 'r')
        kml_file = kmz.open('doc.kml', 'r')
        k = kml.KML()
        k.from_string(kml_file.read())
        main = k.features().next()
        districts = main.features().next()
        for district in districts.features():
            # station.geometry.wkt
            # station.name
            # station.description

            # print district.geometry.wkt
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
            # import ipdb; ipdb.set_trace()
            PollingDistrict.objects.update_or_create(
                council_id=district.id,
                defaults=default_values
            )

