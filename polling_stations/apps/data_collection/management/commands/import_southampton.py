"""
Imports Southampton
"""
from lxml import etree
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from data_collection.management.commands import BaseApiKmlStationsKmlDistrictsImporter

class Command(BaseApiKmlStationsKmlDistrictsImporter):
    """
    Imports the Polling Station data from Southampton
    """
    srid             = 4326
    districts_srid   = 4326
    council_id       = 'E06000045'
    districts_url    = 'http://www.southampton.gov.uk/geoserver/wms?LAYERS=SCC%3APOLLING_DISTRICTS&TRANSPARENT=TRUE&STYLES=Polling_Districts_Labelled&HOVER=false&FORMAT=kml&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG%3A27700&BBOX=436000.0,108500.0,448000.0,118000.0&WIDTH=867&HEIGHT=426'
    stations_url     = 'http://www.southampton.gov.uk/geoserver/wms?LAYERS=SCC%3APOLLING_STATIONS&TRANSPARENT=TRUE&STYLES=Polling_Stations_Labelled&HOVER=false&FORMAT=kml&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG%3A27700&BBOX=436000.0,108500.0,448000.0,118000.0&WIDTH=867&HEIGHT=426'
    elections        = [
        'ref.2016-06-23'
    ]


    def extract_info_from_district_description(self, description):
        # lxml needs everything to be enclosed in one root element
        html = etree.XML('<div>' + str(description).replace('&', '&amp;') + '</div>')
        return {
            'POLLING_DISTRICT_REF': html[1][0][1].text,
            'WARD_NAME':            html[1][1][1].text,
            'TOTAL_ELECTORATE':     html[1][2][1].text,
            'MI_PRINX':             html[1][3][1].text,
        }

    def district_record_to_dict(self, record):
        # polygon
        geojson = record.geom.geojson
        geometry_collection = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))

        try:
            poly = MultiPolygon(geometry_collection[-1])
        except TypeError:
            poly = geometry_collection[-1]

        # metadata
        info = self.extract_info_from_district_description(record['description'])

        return {
            'internal_council_id': info['POLLING_DISTRICT_REF'],
            'name'               : "%s - %s" % (info['WARD_NAME'], info['POLLING_DISTRICT_REF']),
            'area'               : poly
        }

    def extract_info_from_station_description(self, description):
        # lxml needs everything to be enclosed in one root element
        html = etree.XML('<div>' + str(description).replace('&', '&amp;') + '</div>')
        return {
            'POLLING_STATION':      html[1][0][1].text,
            'WARD_NAME':            html[1][1][1].text,
            'POLLING_DISTRICT_REF': html[1][2][1].text,
            'POLLING_STATION_NO':   html[1][3][1].text,
            'MI_PRINX':             html[1][4][1].text,
        }

    def station_record_to_dict(self, record):
        # point
        geojson = record.geom.geojson
        location = GEOSGeometry(geojson, srid=self.get_srid())

        # metadata
        info = self.extract_info_from_station_description(record['description'])

        # format address
        address = info['POLLING_STATION']
        address_parts = address.split(', ')
        if address_parts[-1][:2] == 'SO':
            postcode = address_parts[-1]
            del(address_parts[-1])
        else:
            postcode = ''
        address = "\n".join(address_parts)

        return {
            'internal_council_id': info['POLLING_DISTRICT_REF'],
            'postcode':            postcode,
            'address':             address,
            'location':            location,
            'polling_district_id': info['POLLING_DISTRICT_REF'],
        }
