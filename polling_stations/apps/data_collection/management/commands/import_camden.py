"""
Imports Camden
"""
import json
from lxml import etree
from django.contrib.gis.geos import (
    GEOSGeometry,
    MultiPolygon,
    Point,
    Polygon,
    LinearRing
)
from data_collection.management.commands import (
    BaseGenericApiImporter
)

class Command(BaseGenericApiImporter):
    """
    Imports the Polling Station data from Camden Council
    """
    srid             = 4326
    districts_srid   = 4326
    council_id       = 'E09000007'
    # This isn't GeoJSON - it is JSON with serialised WKT strings embedded in it
    districts_url    = 'https://opendata.camden.gov.uk/api/views/ta65-2szc/rows.json?accessType=DOWNLOAD'
    # This is just a bespoke XML format
    stations_url     = 'https://opendata.camden.gov.uk/api/views/5rhh-fxna/rows.xml?accessType=DOWNLOAD'
    elections        = [
        'gla.c.2016-05-05',
        'gla.a.2016-05-05',
        'mayor.london.2016-05-05',
        'ref.2016-06-23'
    ]

    def convert_linestring_to_multiploygon(self, linestring):
        points = linestring.coords

        # close the LineString so we can transform to LinearRing
        points = list(points)
        points.append(points[0])
        ring = LinearRing(points)

        # now we have a LinearRing we can make a Polygon.. and the rest is simple
        poly = Polygon(ring)
        multipoly = MultiPolygon(poly)
        return multipoly

    def add_districts(self, filename):
        districts = json.load(open(filename))
        for district in districts['data']:
            district_info = self.district_record_to_dict(district)
            district_info['council'] = self.council
            self.add_polling_district(district_info)
        return

    def district_record_to_dict(self, record):
        poly = GEOSGeometry(record[8], srid=self.get_srid('districts'))
        # poly is a LineString, but we need to convert it to a MultiPolygon so it will import
        poly = self.convert_linestring_to_multiploygon(poly)

        return {
            'internal_council_id': record[-1],
            'extra_id': record[-2],
            'name': 'Camden - %s' % (record[-1]),
            'area': poly,
            'polling_station_id': record[-1]
        }

    def add_stations(self, filename):
        xml = etree.parse(filename)
        stations = xml.getroot()[0]
        for station in stations:
            station_info = self.station_record_to_dict(station)
            station_info['council'] = self.council
            self.add_polling_station(station_info)
        return

    def station_record_to_dict(self, record):
        info = {}
        for tag in record:
            info[tag.tag] = tag.text

        address = "\n".join([info['organisation'], info['street']])

        if info['polling_district_name'] == "JA":
            info['postcode'] = "NW5 2HY"
            address = "Rainbow Nursery, St. Benet's Church Hall, Lupton Street London"
            info['longitude'] = "-0.1381025"
            info['latitude'] = "51.554399"

        location = Point(
            float(info['longitude']),
            float(info['latitude']),
            srid=self.get_srid())

        return {
            'internal_council_id': info['polling_district_name'],
            'postcode': info['postcode'],
            'address': address,
            'location': location
        }
