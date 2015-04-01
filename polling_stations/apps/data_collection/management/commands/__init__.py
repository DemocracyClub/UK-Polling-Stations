"""
Defines the base importer classes to override
"""
import json
import glob
import os
import shapefile

from django.core.management.base import BaseCommand
from django.contrib.gis import geos
from django.contrib.gis.geos import Point, GEOSGeometry

from councils.models import Council
from pollingstations.models import PollingStation, PollingDistrict

class BaseImporter(BaseCommand):
    pass

class BaseShpImporter(BaseCommand):
    srid = 27700

    council_id     = None
    stations_name  = "polling_places"
    districts_name = "polling_districts"

    def import_data(self):
        self.import_polling_districts()
        self.import_polling_stations()


    def import_polling_districts(self):
        sf = shapefile.Reader("{0}/{1}".format(
            self.base_folder_path,
            self.districts_name
            ))
        for district in sf.shapeRecords():
            district_info = self.district_record_to_dict(district.record)
            # import ipdb; ipdb.set_trace()

            geojson = json.dumps(district.shape.__geo_interface__)
            poly = self.clean_poly(GEOSGeometry(geojson, srid=self.srid))

            district_info['area'] = poly
            # import ipdb; ipdb.set_trace()
            self.add_polling_district(district_info)

    def add_polling_district(self, district_info):
        PollingDistrict.objects.update_or_create(
            council=self.council,
            internal_council_id=district_info.get('internal_council_id', None),
            defaults=district_info,
        )

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

    def add_polling_station(self, station_info):
        PollingStation.objects.update_or_create(
            council=self.council,
            internal_council_id=station_info['internal_council_id'],
            defaults=station_info,
        )

    def import_polling_stations(self):
        sf = shapefile.Reader("{0}/{1}".format(
            self.base_folder_path,
            self.stations_name
            ))
        for station in sf.shapeRecords():
            station_info = self.station_record_to_dict(station.record)
            station_info['location'] = Point(
                *station.shape.points[0],
                srid=self.srid)
            self.add_polling_station(station_info)



    def handle(self, *args, **kwargs):
        if self.council_id is None:
            self.council_id = args[0]
            
        self.council = Council.objects.get(pk=self.council_id)
        self.base_folder_path = os.path.abspath(
         glob.glob('data/{0}-*'.format(self.council_id))[0]
        )


        self.import_data()






