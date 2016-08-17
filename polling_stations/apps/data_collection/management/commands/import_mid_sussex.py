"""
Imports Mid Sussex
"""
import sys
from lxml import etree
from django.contrib.gis.geos import Point, GEOSGeometry
from data_collection.management.commands import BaseCsvStationsKmlDistrictsImporter

class Command(BaseCsvStationsKmlDistrictsImporter):
    """
    Imports the Polling Station data from Mid Sussex
    """
    council_id     = 'E07000228'
    districts_name = 'msdc_3830_pollingdistricts_polygon.kmz'
    stations_name  = 'R3900_pollingstations.csv'
    elections      = ['parl.2015-05-07']

    def get_station_hash(self, record):
        return "-".join([record.msercode, record.uprn])

    def extract_msercode_from_description(self, description):
        html = etree.HTML(str(description).replace('&', '&amp;'))
        rows = html.xpath("//td")
        return rows[7].text

    def district_record_to_dict(self, record):
        msercode = self.extract_msercode_from_description(record['description'])
        geojson = self.strip_z_values(record.geom.geojson)
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))
        return {
            'internal_council_id': msercode,
            'name'               : record['Name'].value,
            'area'               : poly
        }

    def station_record_to_dict(self, record):

        # KDA is ambiguous: split district?
        if record.msercode == 'KDA':
            return None

        location = Point(float(record.xcoord), float(record.ycoord), srid=self.srid)
        address = "\n".join([record.venue, record.street, record.town])
        return {
            'internal_council_id': record.msercode,
            'postcode':            record.postcode,
            'address':             address,
            'location':            location,
            'polling_district_id': record.msercode
        }
