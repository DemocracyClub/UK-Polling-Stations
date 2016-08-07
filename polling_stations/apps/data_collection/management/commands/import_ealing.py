"""
Imports Ealing
"""
from lxml import etree
from django.contrib.gis.geos import GEOSGeometry
from data_collection.management.commands import BaseApiKmlStationsKmlDistrictsImporter

class Command(BaseApiKmlStationsKmlDistrictsImporter):
    """
    Imports the Polling Station data from Ealing Council
    """
    srid             = 4326
    districts_srid   = 4326
    council_id       = 'E09000009'
    districts_url    = 'http://inspire.misoportal.com/geoserver/london_borough_of_ealing_polling_district_polygon/ows?VERSION=1.1.1&REQUEST=GetMap&SERVICE=WMS&LAYERS=london_borough_of_ealing_polling_district_polygon&STYLES=&BBOX=-0.61059285604864,51.410208305472,0.022513608765178,51.630693143964&SRS=EPSG%3A4258&WIDTH=1005&HEIGHT=349&FORMAT=application/rss+xml&TRANSPARENT=TRUE'
    """
    districts_url isn't KML - it is GeoRSS
    but gdal.DataSource will just deal with it
    because it is made from magic and awesome! :D
    """
    stations_url     = 'http://inspire.misoportal.com/geoserver/london_borough_of_ealing_polling_station_location_point/ows?VERSION=1.1.1&REQUEST=GetMap&SERVICE=WMS&LAYERS=london_borough_of_ealing_polling_station_location_point&STYLES=&BBOX=-0.61059285604864,51.410208305472,0.022513608765178,51.630693143964&SRS=EPSG%3A4258&WIDTH=1005&HEIGHT=349&FORMAT=application/vnd.google-earth.kml+xml&TRANSPARENT=TRUE'
    elections        = [
        'gla.c.2016-05-05',
        'gla.a.2016-05-05',
        'mayor.london.2016-05-05',
        'ref.2016-06-23'
    ]

    def extract_info_from_district_description(self, description):
        # lxml needs everything to be enclosed in one root element
        html = etree.XML('<div>' + str(description).replace('&', '&amp;') + '</div>')
        return {
            'distcode': html[1][0][1].text,
            'wardname': html[1][1][1].text
        }

    def district_record_to_dict(self, record):
        geojson = record.geom.geojson
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))
        info = self.extract_info_from_district_description(record['description'])
        return {
            'internal_council_id': info['distcode'],
            'name'               : "%s - %s" % (info['wardname'], info['distcode']),
            'area'               : poly
        }

    def extract_info_from_station_description(self, description):
        # lxml needs everything to be enclosed in one root element
        html = etree.XML('<div>' + str(description).replace('&', '&amp;') + '</div>')
        data = {
            'polling_station': html[1][0][1].text,
            'pollingdistrict': html[1][1][1].text,
            'mi_ss':           html[1][2][1].text,
        }
        return data

    def station_record_to_dict(self, record):
        geojson = record.geom.geojson
        location = GEOSGeometry(geojson, srid=self.get_srid())
        info = self.extract_info_from_station_description(record['description'])
        return {
            'internal_council_id': info['pollingdistrict'],
            'postcode':            '',
            'address':             info['polling_station'],
            'location':            location,
            'polling_district_id': info['pollingdistrict']
        }
