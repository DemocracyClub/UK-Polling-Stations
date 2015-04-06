"""
Imports Spelthorne Council.
"""
import json 

from django.contrib.gis.geos import Point, GEOSGeometry
import ffs

from data_collection.management.commands import BaseKamlImporter

class Command(BaseKamlImporter):
    """
    Imports the Polling Station data from Spelthorne Council
    """
    council_id     = 'E07000213'
    districts_name = 'Polling_Districts.kmz'
    stations_name  = 'Polling_Stations.csv'

    def import_data(self):
        """
        There are two types of import - districts and stations.
        """
        for dist in self.council.pollingdistrict_set.all():
            dist.delete()
        self.import_polling_districts()
        self.import_polling_stations()

    
    def strip_z_values(self, geojson):
        districts = json.loads(geojson)
        districts['type'] = 'Polygon'
        for points in districts['coordinates'][0][0]:
            if len(points) == 3:
                points.pop()
        districts['coordinates'] = districts['coordinates'][0]
        return json.dumps(districts)


    def district_record_to_dict(self, record):
        geojson = self.strip_z_values(record.geom.geojson)
        # Th SRID for the KML is 4326 but the CSV is 2770 so we
        # set it each time we create the polygon.
        # We could probably do with a more elegant way of doing
        # this longer term, but as this is the frist KML importer
        # we're weiting to abstract it
        self._srid = self.srid
        self.srid = 4326
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.srid))
        self.srid = self._srid
        return {
            'internal_council_id': record['Name'].value,
            'name'               : record['Name'].value,
            'area'               : poly
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.point_x), int(record.point_y), srid=self.srid)
        except ValueError:
            location = Point(float(record.point_x), float(record.point_y), srid=self.srid)
        return {
            'internal_council_id': record.polling_di,
            'postcode': '(no postcode)',
            'address': "\n".join([record.building, record.road, record.town_villa]),
            'location': location
        }
