"""
Imports Ryedale
"""
from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseKamlImporter

class Command(BaseKamlImporter):
    """
    Imports the Polling Station data from Ryedale Council
    """
    council_id     = 'E07000167'
    districts_name = 'Thirsk_and_Malton_Wards.kml'
    stations_name  = 'Polling Stations Malton and Thirsk 07 05 2015.csv'

    def district_record_to_dict(self, record):
        # this kml has no altitude co-ordinates so the data is ok as it stands
        geojson = record.geom.geojson

        # The SRID for the KML is 4326 but the CSV is 2770 so we
        # set it each time we create the polygon.
        # We could probably do with a more elegant way of doing
        # this longer term.
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
        location = Point(float(record.easting), float(record.northin), srid=self.srid)
        address_parts = record.address.split(' ')
        address = ' '.join(address_parts[:-2])
        return {
            'internal_council_id': record.postcode, # no id supplied, so we'll use the postcode
            'postcode':            record.postcode,
            'address':             address,
            'location':            location
        }
