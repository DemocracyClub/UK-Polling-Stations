import os
import glob

from django.core.management.base import BaseCommand
from django.contrib.gis import geos

from councils.models import Council

class BaseImporter(BaseCommand):
    pass

class BaseShpImporter(BaseCommand):
    stations_name = "polling_places"
    districts_name = "polling_districts"

    def clean_poly(self, poly):
        # print wkt
        # import ipdb; ipdb.set_trace()
        if isinstance(poly, geos.Polygon):
            poly = geos.MultiPolygon(poly, srid=self.srid)
            return poly
        # import ipdb; ipdb.set_trace()

        # try:
        #     polygons = wkt[18:-3].split(')), ((')
        #     WKT = ""
        #     for polygon in polygons:
        #         points = polygon.split(',')
        #         cleaned_points = ""
        #         for point in points:
        #             split_points = point.strip().split(' ')
        #             x = split_points[0]
        #             y = split_points[1]
        #             cleaned_points += "%s %s, " % (x,y)
        #         cleaned_points = "((%s))," % cleaned_points[:-2]
        #
        #         WKT += cleaned_points
        # except:
        #     WKT = wkt
        #
        # WKT = "MULTIPOLYGON (%s)" % wkt
        # print WKT
        return poly


    def handle(self, *args, **kwargs):
        self.council_id = args[0]
        self.council = Council.objects.get(pk=self.council_id)
        self.base_folder_path = os.path.abspath(
         glob.glob('data/{0}-*'.format(self.council_id))[0]
        )


        self.import_data()

