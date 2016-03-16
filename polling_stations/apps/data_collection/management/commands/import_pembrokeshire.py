"""
Imports Pembrokeshire
"""
from lxml import etree
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from data_collection.management.commands import BaseApiKmlKmlImporter

class Command(BaseApiKmlKmlImporter):
    """
    Imports the Polling Station data from Pembrokeshire
    """
    srid             = 4326
    districts_srid   = 4326
    council_id       = 'W06000009'
    districts_url    = 'http://www.pembrokeshire.gov.uk/geoserver/maps/live/wms?LAYERS=tblPollingDistrict&FORMAT=application/vnd.google-earth.kml+xml&TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&SRS=EPSG%3A27700&BBOX=162666.9591241047,187007.85481671634,234800.000001,260094.71375428123&WIDTH=256&HEIGHT=256'
    stations_url     = 'http://www.pembrokeshire.gov.uk/geoserver/maps/live/wms?LAYERS=tblPollingStation&FORMAT=application/vnd.google-earth.kml+xml&TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&SRS=EPSG%3A27700&BBOX=162666.9591241047,187007.85481671634,234800.000001,260094.71375428123&WIDTH=256&HEIGHT=256'

    def extract_info_from_district_description(self, description):
        # lxml needs everything to be enclosed in one root element
        html = etree.XML('<div>' + str(description).replace('&', '&amp;') + '</div>')
        return {
            'district_id':   html[1][0][1].text,
            'district_code': html[1][1][1].text,
            'name_en':       html[1][2][1].text,
            'name_cy':       html[1][3][1].text,
        }

    def district_record_to_dict(self, record):
        geojson = record.geom.geojson
        geometry_collection = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))

        try:
            poly = MultiPolygon(geometry_collection[-1])
        except TypeError:
            poly = geometry_collection[-1]

        info = self.extract_info_from_district_description(record['description'])

        return {
            'internal_council_id': info['district_code'],
            'name'               : "%s / %s" % (info['name_en'], info['name_cy']),
            'extra_id'           : info['district_id'],
            'area'               : poly
        }


    def extract_info_from_station_description(self, description):
        # lxml needs everything to be enclosed in one root element
        html = etree.XML('<div>' + str(description).replace('&', '&amp;') + '</div>')
        data = {
            'id':      html[1][0][1].text,
            'name_en': html[1][1][1].text,
            'name_cy': html[1][2][1].text,
        }
        return data

    def station_record_to_dict(self, record):
        geojson = record.geom.geojson
        location = GEOSGeometry(geojson, srid=self.get_srid())
        info = self.extract_info_from_station_description(record['description'])
        internal_id = record['Name'].value.split(".")[1]

        # address data is too poor to produce useful results using geocoding
        postcode = ''

        return {
            'internal_council_id': internal_id,
            'postcode':            postcode,
            'address':             "%s / %s" % (info['name_en'], info['name_cy']),
            'location':            location
        }
