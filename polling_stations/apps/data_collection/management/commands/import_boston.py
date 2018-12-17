"""
Import Boston
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsShpDistrictsImporter

class Command(BaseCsvStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Boston Council
    """
    council_id = 'E07000136'
    districts_name = 'Polling Districts May 2015_region'
    stations_name = 'pollingstations.csv'
    elections = ['parl.2015-05-07']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': "%s - %s" % (record[1], record[0]),
            'polling_station_id': record[0]
        }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.easting), int(record.northing), srid=self.srid)
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.srid)

        address_parts = [x.strip() for x in record.address.split(',')]
        address = "\n".join(address_parts[:-1])
        postcode = address_parts[-1]

        """
        In this data, sometimes a single polling station serves several
        districts. For simplicity, if record.internal_id is something like "AB,AC" 
        return the same polling station address/point multiple times with different IDs
        """
        internal_ids = record.internal_id.split(",")
        if (len(internal_ids) == 1):
            return {
                'internal_council_id': record.internal_id,
                'postcode'           : postcode,
                'address'            : address,
                'location'           : location
            }
        else:
            stations = []
            for id in internal_ids:
                stations.append({
                    'internal_council_id': id,
                    'postcode'           : postcode,
                    'address'            : address,
                    'location'           : location
                })
            return stations
