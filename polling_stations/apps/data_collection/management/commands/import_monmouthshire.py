from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'W06000021'
    districts_name = 'polling_district'
    stations_name = 'polling_station.shp'
    elections = ['local.monmouthshire.2017-05-04']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[1]).strip(),
            'name': str(record[1]).strip(),
            'polling_station_id': record[3]
        }

    def station_record_to_dict(self, record):

        station = {
            'internal_council_id': record[0],
            'postcode'           : '',
            'address'            : "%s\n%s" % (record[2].strip(), record[4].strip()),
        }

        if str(record[1]).strip() == '10033354925':
            """
            There is a dodgy point in this file.
            It has too many digits for a UK national grid reference.

            (Either that or Bwttws Newydd Parish Community Hall
            is actually in the sea somewhere between Norway and Iceland)

            Replace it with the point for the postcode centroid
            """
            station['location'] = Point(336103, 205979, srid=27700)

        return station
