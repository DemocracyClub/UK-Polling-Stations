"""
Importer for Gravesham
"""
import json

from django.contrib.gis.geos import GEOSGeometry, Point

from data_collection.management.commands import BaseKamlImporter

class Command(BaseKamlImporter):
    council_id = 'E07000109'
    districts_name = 'PollingDistricts2015.kml'
    stations_name  = 'Polling Stations 2015.csv'

    def strip_z_values(self, geojson):
        districts = json.loads(geojson)
        districts['type'] = 'Polygon'
        for points in districts['coordinates'][0][0]:
            if len(points) == 3:
                points.pop()
        districts['coordinates'] = [districts['coordinates'][0][0]]
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
            location = Point(int(record.easting), int(record.northing), srid=self.srid)
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.srid)
        return {
            'internal_council_id': record.polling_district,
            'postcode': record.address.split(',')[-1],
            'address': "\n".join(record.address.decode('Latin-1').split(',')[:-1]),
            'location': location
        }
