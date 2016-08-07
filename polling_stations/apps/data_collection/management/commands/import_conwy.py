"""
Import Conwy
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsShpDistrictsImporter

class Command(BaseCsvStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Conwy Council
    """
    council_id     = 'W06000003'
    districts_name = 'Conwy CBC Polling Districts 20160407'
    stations_name  = 'Conwy CBC Polling Stations (with UPRN) 20160407.csv'
    elections      = [
        'pcc.2016-05-05',
        'naw.c.2016-05-05',
        'naw.r.2016-05-05',
        'ref.2016-06-23'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[5],
            'name': record[4],
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.easting), int(record.northing), srid=self.get_srid())
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.get_srid())

        postcode = record.polling_station_address.split(', ')[-1]
        address = "\n".join(record.polling_station_address.split(', ')[:-1])

        return {
            'internal_council_id': record.districts,
            'postcode'           : postcode,
            'address'            : address,
            'polling_district_id': record.districts,
            'location'           : location
        }
