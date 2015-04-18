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
